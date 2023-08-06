##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""PostgreSQL adapter for RelStorage."""
from __future__ import absolute_import

import logging
import re

from zope.interface import implementer

from ...options import Options
from .._abstract_drivers import _select_driver
from .._util import query_property
from ..dbiter import HistoryFreeDatabaseIterator
from ..dbiter import HistoryPreservingDatabaseIterator
from ..interfaces import IRelStorageAdapter
from ..packundo import HistoryFreePackUndo
from ..packundo import HistoryPreservingPackUndo
from ..poller import Poller
from ..scriptrunner import ScriptRunner
from . import drivers
from .connmanager import Psycopg2ConnectionManager
from .locker import PostgreSQLLocker
from .mover import PG8000ObjectMover
from .mover import PostgreSQLObjectMover
from .mover import to_prepared_queries
from .oidallocator import PostgreSQLOIDAllocator
from .schema import PostgreSQLSchemaInstaller
from .stats import PostgreSQLStats
from .txncontrol import PostgreSQLTransactionControl

log = logging.getLogger(__name__)

def select_driver(options=None):
    return _select_driver(options or Options(), drivers)

@implementer(IRelStorageAdapter)
class PostgreSQLAdapter(object):
    """PostgreSQL adapter for RelStorage."""

    # pylint:disable=too-many-instance-attributes
    def __init__(self, dsn='', options=None):
        # options is a relstorage.options.Options or None
        self._dsn = dsn
        if options is None:
            options = Options()
        self.options = options
        self.keep_history = options.keep_history
        self.version_detector = PostgreSQLVersionDetector()

        self.driver = driver = select_driver(options)
        log.debug("Using driver %r", driver)

        self.connmanager = Psycopg2ConnectionManager(
            driver,
            dsn=dsn,
            options=options,
        )
        self.runner = ScriptRunner()
        self.locker = PostgreSQLLocker(
            options=options,
            lock_exceptions=driver.lock_exceptions,
            version_detector=self.version_detector,
        )
        self.schema = PostgreSQLSchemaInstaller(
            connmanager=self.connmanager,
            runner=self.runner,
            locker=self.locker,
            keep_history=self.keep_history,
        )

        mover_type = PostgreSQLObjectMover
        if driver.__name__ == 'pg8000':
            mover_type = PG8000ObjectMover

        self.mover = mover_type(
            driver,
            options=options,
            runner=self.runner,
            version_detector=self.version_detector,
        )
        self.connmanager.add_on_store_opened(self.mover.on_store_opened)
        self.connmanager.add_on_load_opened(self.mover.on_load_opened)
        self.oidallocator = PostgreSQLOIDAllocator()
        self.txncontrol = PostgreSQLTransactionControl(
            keep_history=self.keep_history,
            driver=driver,
        )

        self.poller = Poller(
            poll_query="EXECUTE get_latest_tid",
            keep_history=self.keep_history,
            runner=self.runner,
            revert_when_stale=options.revert_when_stale,
        )
        self.connmanager.add_on_load_opened(self._prepare_get_latest_tid)
        self.connmanager.add_on_store_opened(self._prepare_get_latest_tid)

        if self.keep_history:
            self.packundo = HistoryPreservingPackUndo(
                driver,
                connmanager=self.connmanager,
                runner=self.runner,
                locker=self.locker,
                options=options,
            )
            self.dbiter = HistoryPreservingDatabaseIterator(
                driver,
                runner=self.runner,
            )
        else:
            self.packundo = HistoryFreePackUndo(
                driver,
                connmanager=self.connmanager,
                runner=self.runner,
                locker=self.locker,
                options=options,
            )
            self.dbiter = HistoryFreeDatabaseIterator(
                driver,
                runner=self.runner,
            )

        self.stats = PostgreSQLStats(
            connmanager=self.connmanager,
            keep_history=self.keep_history
        )

    _get_latest_tid_queries = (
        """
        SELECT tid
        FROM transaction
        ORDER BY tid DESC
        LIMIT 1
        """,
        """
        SELECT tid
        FROM object_state
        ORDER BY tid DESC
        LIMIT 1
        """
    )

    _prepare_get_latest_tid_queries = to_prepared_queries(
        'get_latest_tid',
        _get_latest_tid_queries)

    _prepare_get_latest_tid_query = query_property('_prepare_get_latest_tid')

    def _prepare_get_latest_tid(self, cursor, restart=False):
        if restart:
            return
        stmt = self._prepare_get_latest_tid_query
        cursor.execute(stmt)

    def new_instance(self):
        inst = type(self)(dsn=self._dsn, options=self.options)
        inst.version_detector.version = self.version_detector.version
        return inst

    def __str__(self):
        parts = [self.__class__.__name__]
        if self.keep_history:
            parts.append('history preserving')
        else:
            parts.append('history free')
        dsnparts = self._dsn.split()
        s = ' '.join(p for p in dsnparts if not p.startswith('password'))
        parts.append('dsn=%r' % s)
        return ", ".join(parts)



class PostgreSQLVersionDetector(object):

    version = None

    def get_version(self, cursor):
        """Return the (major, minor) version of the database"""
        if self.version is None:
            cursor.execute("SELECT version()")
            v = cursor.fetchone()[0]
            m = re.search(r"([0-9]+)[.]([0-9]+)", v)
            if m is None:
                raise AssertionError("Unable to detect database version: " + v)
            self.version = int(m.group(1)), int(m.group(2))
        return self.version
