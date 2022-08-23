from sqlite_to_postgres.tests.check_consistency.resources import \
    TABLE_NAME_REQUEST, TABLES, TABLE_CLASSES
import os
import sqlite3

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

load_dotenv()

DSL = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'options': '-c search_path=content'
}


class Connector:
    def __init__(self, conn, table_name):
        self.connection = conn
        self.table_name = table_name
        self.curs = self.connection.cursor()

    def count_record(self):
        self.curs.execute(f"SELECT * FROM {self.table_name};")
        return len(self.curs.fetchall())

    def record(self):
        self.curs.execute(TABLE_NAME_REQUEST[self.table_name])
        return self.curs.fetchall()


def test_count_reqords():
    for table_name in TABLES:
        with sqlite3.connect('db.sqlite') as sqlite_conn,\
                psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
            assert Connector(
                sqlite_conn, table_name).count_record() == Connector(
                pg_conn, table_name).count_record()


def test_matching_records():
    with sqlite3.connect('db.sqlite') as sqlite_conn,\
            psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
        data_sqlite = Connector(sqlite_conn, 'film_work').record()
        data_postgre = Connector(pg_conn, 'film_work').record()
        result_sqlite = []
        result_postgre = []
        for _ in data_sqlite:
            obj = TABLE_CLASSES['film_work'](*_)
            obj.created_at = obj.created_at.partition('.')[0]
            if obj.updated_at:
                obj.updated_at = obj.updated_at.partition('.')[0]
            result_sqlite.append(obj)
        for _ in data_postgre:
            obj_po = TABLE_CLASSES['film_work'](*_)
            obj_po.created_at = obj_po.created_at.strftime('%Y-%m-%d %H:%M:%S')
            if obj_po.updated_at:
                obj_po.updated_at = obj_po.updated_at.strftime(
                    '%Y-%m-%d %H:%M:%S')
            result_postgre.append(obj_po)
        for _ in range(len(result_sqlite)):
            assert result_sqlite[_] == result_postgre[_]


if __name__ == '__main__':
    # test_matching_records()
    test_count_reqords()
