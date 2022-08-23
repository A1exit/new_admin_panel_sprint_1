from sqlite_to_postgres.data_classes import (Filmwork, Genre, GenreFilmwork,
                                             Person, PersonFilmwork)

TABLE_CLASSES = {
    'film_work': Filmwork,
    'genre': Genre,
    'genre_film_work': GenreFilmwork,
    'person': Person,
    'person_film_work': PersonFilmwork
}
TABLES = ['film_work', 'genre', 'genre_film_work', 'person',
          'person_film_work']
BLOCK_SIZE = 100
TABLE_NAME_COLUMN = {
    'film_work': (
        'id',
        'title',
        'description',
        'creation_date',
        'file_path',
        'rating',
        'type',
        'created_at',
        'updated_at'),
    'genre': (
        'id',
        'name',
        'description',
        'created_at',
        'updated_at'),
    'genre_film_work': (
        'id',
        'film_work_id',
        'genre_id',
        'created'),
    'person': (
        'id',
        'full_name',
        'created_at',
        'updated_at'),
    'person_film_work': (
        'id',
        'film_work_id',
        'person_id',
        'role',
        'created_at')}

TABLE_NAME_REQUEST = {
    'film_work': "SELECT id, title, description, creation_date, file_path,"
                 "rating, type, created_at, updated_at FROM film_work;",
    'genre': "SELECT id, name, description, created_at,"
             "updated_at FROM genre;",
    'genre_film_work': "SELECT id, film_work_id, genre_id,"
                       "created_at FROM genre_film_work;",
    'person': "SELECT id, full_name, created_at, updated_at FROM person;",
    'person_film_work': "SELECT id, film_work_id, person_id, role,"
                        "created_at FROM person;",
}
