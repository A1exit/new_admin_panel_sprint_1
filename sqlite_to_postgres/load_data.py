import os
import sqlite3

import psycopg2
import logging
from dotenv import load_dotenv
from loader_clsss import PostgresSaver, SQLiteLoader
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from sqlite_to_postgres.resources import TABLE_CLASSES

load_dotenv()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    for table_name, data_class in TABLE_CLASSES.items():
        try:
            sqlite_loader = SQLiteLoader(connection, table_name, data_class)
            data = sqlite_loader.load_movies()
        except sqlite3.IntegrityError:
            logging.error("couldn't add Python twice")
            break
        try:
            postgres_saver = PostgresSaver(pg_conn, table_name, data_class)
            postgres_saver.save_all_data(data)
        except sqlite3.IntegrityError:
            logging.error("couldn't add Python twice")
            break


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

    sqlite_conn.close()
    pg_conn.close()
