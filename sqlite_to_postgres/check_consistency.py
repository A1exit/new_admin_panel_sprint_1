import sqlite3

import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection

from resources import TABLES


class Connector:
    def __init__(self, conn, table_name):
        self.connection = conn
        self.table_name = table_name
        self.curs = self.connection.cursor()


class SQLite_loader(Connector):
    def count_record_sqlite(self, sqlite_conn):
        db_path = 'db.sqlite'
        conn = sqlite3.connect(db_path)
        curs = conn.cursor()
        curs.execute("SELECT * FROM film_work;")
        data = curs.fetchall()
        conn.close()


class Postgre_loader(Connector):
    def count_record_postgre(self, pg_conn):
        db_path = 'db.sqlite'
        conn = sqlite3.connect(db_path)
        curs = conn.cursor()
        curs.execute("SELECT * FROM film_work;")
        data = curs.fetchall()
        conn.close()


# def test_answer():
#     assert func(3) == 5

def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    for table_name in TABLES:
        connector = SQLite_loader(connection, table_name=table_name)
        connector.count_record_sqlite()


if __name__ == '__main__':
    dsl = {
        'dbname': 'movies_database',
        'user': 'app',
        'password': '123qwe',
        'host': '127.0.0.1',
        'port': 5432,
        'options': '-c search_path=content'
           }

    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(
            **dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)