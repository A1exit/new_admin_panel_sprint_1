CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creations_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    FOREIGN KEY (genre_id) REFERENCES genre (genre_id),
    FOREIGN KEY (film_work_id) REFERENCES film_work (film_work_id),
    created timestamp with time zone
);

CREATE UNIQUE INDEX film_work_person_idx ON
    content.genre_film_work (film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    FOREIGN KEY (film_work_id) REFERENCES film_work (film_work_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    role TEXT NOT NULL,
    created timestamp with time zone
);

CREATE UNIQUE INDEX film_work_person_idx ON
    content.person_film_work (film_work_id, person_id);


