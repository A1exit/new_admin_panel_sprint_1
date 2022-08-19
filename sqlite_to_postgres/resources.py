from data_classes import (Filmwork, Genre, GenreFilmwork, PersonFilmwork,
                          Person)

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
    'film_work': ('id', 'title', 'description', 'creation_date', 'file_path', 'rating', 'type', 'created', 'modified'),
    'genre': ('id', 'name', 'description', 'created', 'modified'),
    'genre_film_work': ('id', 'film_work_id', 'genre_id', 'created'),
    'person': ('id', 'full_name', 'created', 'modified'),
    'person_film_work': ('id', 'film_work_id', 'person_id', 'role', 'created')
}