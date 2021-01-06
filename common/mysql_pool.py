import pymysql

import settings
from manager import MODEL

from apps.wechat_mp.config import MiniProgram


class ConnMysql(object):

    def __init__(
            self,
            db=MiniProgram.DATABASE, host=settings.config_map[MODEL].HOST,
            port=settings.config_map[MODEL].MYSQL_PORT,
            user=settings.config_map[MODEL].MYSQL_USER,
            pwd=settings.config_map[MODEL].MYSQL_PWD, charset="utf8"
    ) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db
        self.charset = charset
        self.init()

    def init(self):
        self.conn_mysql = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.pwd,
            db=self.db,
            charset=self.charset
        )
        self.cursor = self.conn_mysql.cursor()

    def query(self, sql, params):

        res = self.cursor.execute(sql, params)
        # record = self.cursor.fetchone()
        records = self.cursor.fetchall()
        self.close()

        return res, records  # 此时以元组的形式返回

    def insert(self, sql, params):
        try:
            res = self.cursor.execute(sql, params)
            self.conn_mysql.commit()

            return res, None

        except Exception as e:
            self.conn_mysql.rollback()

            return False, e

        finally:
            self.close()

    def delete(self, sql, params):
        try:
            res = self.cursor.execute(sql, params)
            self.conn_mysql.commit()

            return res, None

        except Exception as e:
            self.conn_mysql.rollback()

            return False, e

        finally:
            self.close()

    def update(self, sql, params):
        try:
            res = self.cursor.execute(sql, params)
            self.conn_mysql.commit()

            return res, None

        except Exception as e:
            self.conn_mysql.rollback()

            return False, e

        finally:
            self.close()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn_mysql:
            self.conn_mysql.close()
