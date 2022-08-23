from sqlite_to_postgres.tests.check_consistency.resources import (
    BLOCK_SIZE, TABLE_CLASSES, TABLE_NAME_COLUMN, TABLES)
import io
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

load_dotenv()


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()


class SQLiteLoader:
    def __init__(self, conn: sqlite3.Connection, table_name):
        self.connection = conn
        self.table_name = table_name
        self.curs = self.connection.cursor()

    def load_movies(self):
        self.curs.execute(f'SELECT * FROM {self.table_name};')
        while True:
            data = self.curs.fetchmany(size=BLOCK_SIZE)
            if not data:
                break
            result = []
            for _ in data:
                obj = TABLE_CLASSES[self.table_name](*_)
                result.append(obj)
            yield result


class PostgresSaver(SQLiteLoader):
    def save_all_data(self, data):
        for block in data:
            values = '\n'.join(
                ['\t'.join([str(x) for x in asdict(obj).values()]) for
                 obj in block])
            with io.StringIO(values) as f:
                self.curs.copy_from(f,
                                    table=self.table_name,
                                    null='None',
                                    columns=TABLE_NAME_COLUMN[self.table_name],
                                    size=BLOCK_SIZE)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    for table_name in TABLES:
        sqlite_loader = SQLiteLoader(connection, table_name)
        data = sqlite_loader.load_movies()
        postgres_saver = PostgresSaver(pg_conn, table_name)
        postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'options': '-c search_path=content'
    }

    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(
            **dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
