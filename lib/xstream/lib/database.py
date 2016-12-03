# -*- coding: utf-8 -*-
from datetime import datetime
import os
from xstream import common
from xstream.lib import logger

try:
    from sqlite3 import dbapi2 as database
    logger.info('Loading sqlite3 as DB engine version: %s' % database.sqlite_version)
except:
    from pysqlite2 import dbapi2 as database
    logger.info('pysqlite2 as DB engine')


class Database:
    def __init__(self):
        self.cache_db = os.path.join(common.profile_path, 'cache.db')

        self.dbcon = database.connect(self.cache_db)
        self.dbcon.row_factory = database.Row
        self.dbcur = self.dbcon.cursor()

        self._init_net_cache()

    def _init_net_cache(self):
        sql_create = "CREATE TABLE IF NOT EXISTS net_cache (" \
                     "url TEXT PRIMARY KEY, " \
                     "code TEXT, " \
                     "msg TEXT, " \
                     "hdrs TEXT, " \
                     "body TEXT," \
                     "[timestamp] TIMESTAMP" \
                     ");"

        self.dbcur.execute(sql_create)

    def insert_response(self, url, code, msg, hdrs, body):
        sql_insert = "INSERT INTO net_cache (url, code, msg, hdrs, body, [timestamp]) VALUES (?,?,?,?,?,?)"

        try:
            self.dbcur.execute(sql_insert, (url, code, msg, hdrs, body, datetime.now()))
            self.dbcon.commit()
        except Exception, e:
            logger.info('************* Error inserting into cache db: %s' % e)
            return

    def select_response(self, url, cache_time=0):
        sql_select = "SELECT * FROM net_cache WHERE url = '%s'" % url

        try:
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchone()
        except Exception, e:
            logger.info('************* Error selecting from cache db: %s' % e)
            return None

        if matchedrow:
            if cache_time > 0:
                pass
            else:
                logger.info('Found url in cache table: %s' % dict(matchedrow))
                return dict(matchedrow)
        else:
            logger.info('No match in local DB for url: %s' % url)
            return False