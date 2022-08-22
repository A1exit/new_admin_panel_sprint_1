import sqlite3
import os

import psycopg2
from psycopg2.extras import DictCursor

DSL = {
        'dbname': 'movies_database',
        'user': 'app',
        'password': '123qwe',
        'host': '127.0.0.1',
        'port': 5432,
        'options': '-c search_path=content'
           }

DB_PATH = '../../db.sqlite'

TABLES = ['film_work', 'genre', 'genre_film_work', 'person',
          'person_film_work']


class Connector:
    def __init__(self, conn, table_name):
        self.connection = conn
        self.table_name = table_name
        self.curs = self.connection.cursor()

    def count_record(self):
        self.curs.execute(f"SELECT * FROM {self.table_name};")
        return len(self.curs.fetchall())

    def record(self):
        self.curs.execute(f"SELECT * FROM {self.table_name};")
        return self.curs.fetchall()


def test_count_reqords():
    for table_name in TABLES:
        with sqlite3.connect(DB_PATH) as sqlite_conn,\
                psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
            assert Connector(sqlite_conn, table_name).count_record() == Connector(pg_conn, table_name).count_record()


def test_matching_records():
    for table_name in TABLES:
        with sqlite3.connect('../../db.sqlite') as sqlite_conn,\
                psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
            data_sqlite = Connector(sqlite_conn, table_name).record()
            data_postgre = Connector(pg_conn, table_name).record()
            return data_sqlite, data_postgre


if __name__ == '__main__':
    test_matching_records()
