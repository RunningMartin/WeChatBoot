import logging
import sqlite3
from src import config

logger = logging.getLogger(__name__)


class DataBase(object):
    @classmethod
    def init_database(cls):
        connect = sqlite3.connect(config.DATABASE_NAME)
        cursor = connect.cursor()
        logger.info("init database")
        logger.info("init chat table")
        logger.info(config.CREATE_CHAT_TABLE_SQL)
        cursor.execute(config.CREATE_CHAT_TABLE_SQL)
        connect.commit()

        logger.info("init admin table")
        logger.info(config.CREATE_ADMIN_SQL)
        cursor.execute(config.CREATE_ADMIN_SQL)
        connect.commit()

        logger.info("init chat_group table")
        logger.info(config.CREATE_LISTEN_CHAT_GROUP_SQL)
        cursor.execute(config.CREATE_LISTEN_CHAT_GROUP_SQL)
        connect.commit()
        connect.close()

    @classmethod
    def save_chat(cls, group, sender, time, content):
        connect = sqlite3.connect(config.DATABASE_NAME)
        cursor = connect.cursor()
        sql = config.INSERT_CHAT_SQL.format(group, sender, time, content)
        logger.info("insert chat")
        logger.info(sql)
        cursor.execute(sql)
        connect.commit()
        connect.close()

    @classmethod
    def add_admin(cls, admin_id, chat_group, admin_name):
        connect = sqlite3.connect(config.DATABASE_NAME)
        cursor = connect.cursor()
        sql = config.INSERT_ADMIN_SQL.format(admin_id, chat_group, admin_name)
        logger.info("insert admin")
        logger.info(sql)
        cursor.execute(sql)
        connect.commit()
        connect.close()

    @classmethod
    def all_admin(cls, chat_group=None):
        connect = sqlite3.connect(config.DATABASE_NAME)
        cursor = connect.cursor()
        logger.info("query all admin")
        if chat_group:
            sql = config.QUERY_GROUP_ADMIN_SQL.format(chat_group)
        else:
            sql = config.QUERY_ADMIN_SQL

        logger.info(sql)
        rows = cursor.execute(sql)
        result = [row[0] for row in rows if row]
        connect.close()

        return result

    @classmethod
    def delete_admin(cls, admin_id, group):
        connect = sqlite3.connect(config.DATABASE_NAME)
        cursor = connect.cursor()
        sql = config.DELETE_ADMIN_SQL.format(admin_id, group)
        logger.info("delete admin")
        logger.info(sql)
        cursor.execute(sql)
        connect.commit()
        connect.close()

    @classmethod
    def add_listen_group(cls, puid, chat_group):
        connect = sqlite3.connect(config.DATABASE_NAME)
        cursor = connect.cursor()
        sql = config.INSERT_LISTEN_CHAT_GROUP_SQL.format(puid, chat_group)
        logger.info("insert listen group")
        logger.info(sql)
        cursor.execute(sql)
        connect.commit()
        connect.close()

    @classmethod
    def all_listen_group(cls):
        connect = sqlite3.connect(config.DATABASE_NAME)
        cursor = connect.cursor()
        logger.info("query all listen group")
        sql = config.QUERY_LISTEN_CHAT_GROUP_SQL
        logger.info(sql)
        rows = cursor.execute(sql)
        result = [row[0] for row in rows if row]
        connect.close()

        return result

    @classmethod
    def delete_listen_group(cls, puid):
        connect = sqlite3.connect(config.DATABASE_NAME)
        cursor = connect.cursor()
        sql = config.DELETE_LISTEN_CHAT_GROUP_SQL.format(puid)
        logger.info("delete listen group")
        logger.info(sql)
        cursor.execute(sql)
        connect.commit()
        connect.close()

    @classmethod
    def count_member_by_date(cls, group_name, start_date, end_date):
        connect = sqlite3.connect(config.DATABASE_NAME)
        cursor = connect.cursor()
        sql = config.QUERY_CHAT_BY_DATA_SQL.format(group_name, start_date, end_date)
        logger.info("count member")
        logger.info(sql)
        rows = cursor.execute(sql)
        result = [row[0] for row in rows if row]
        connect.close()

        return result
