from dataclasses import dataclass, asdict


@dataclass
class Filmwork:
    __slots__ = (
        'id', 'title', 'description', 'creation_date', 'file_path', 'rating',
        'type',
        'created_at', 'updated_at'
    )
    id: str
    title: str
    description: str
    creation_date: str
    file_path: str
    rating: float
    type: str
    created_at: str
    updated_at: str


@dataclass
class Genre:
    __slots__ = (
        'id', 'name', 'description', 'created_at', 'updated_at'
    )
    id: str
    name: str
    description: str
    created_at: str
    updated_at: str


@dataclass
class GenreFilmwork:
    __slots__ = (
        'id', 'film_work_id', 'genre_id', 'created_at'
    )
    id: str
    film_work_id: str
    genre_id: str
    created_at: str


@dataclass
class Person:
    __slots__ = (
        'id', 'full_name', 'created', 'updated_at'
    )
    id: str
    full_name: str
    created: str
    updated_at: str


@dataclass
class PersonFilmwork:
    __slots__ = (
        'id', 'film_work_id', 'person_id', 'role', 'created_at'
    )
    id: str
    film_work_id: str
    person_id: str
    role: str
    created_at: str
