import io
import sqlite3
from dataclasses import asdict

from sqlite_to_postgres.resources import BLOCK_SIZE, TABLE_NAME_COLUMN


class SQLiteLoader:
    def __init__(self, conn: sqlite3.Connection, table_name, data_class):
        self.connection = conn
        self.table_name = table_name
        self.data_class = data_class
        self.curs = self.connection.cursor()

    def load_movies(self):
        self.curs.execute(f'SELECT {", ".join(self.data_class.__slots__)} '
                          f'FROM {self.table_name};')
        while data := self.curs.fetchmany(size=BLOCK_SIZE):
            yield [self.data_class(*row) for row in data]


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
