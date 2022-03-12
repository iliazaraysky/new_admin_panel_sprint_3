import os
import logging
import psycopg2
from dotenv import load_dotenv
from check_data_change import set_set_last_change_date


log_folder = os.path.abspath('logs')
log_name = 'postgres_extract.log'
log_file = os.path.join(log_folder, log_name)


logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

load_dotenv()

dsl = {
        'dbname': os.getenv('POSTGRESQL_DB'),
        'user': os.getenv('POSTGRESQL_USER'),
        'password': os.getenv('POSTGRESQL_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
}


def retrieve_data_from_postgres(dsl):
    conn = psycopg2.connect(**dsl)
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT film_work.id,
        film_work.rating AS imdb_rating,
        ARRAY_AGG(DISTINCT genre.name) AS genre,
        film_work.title,
        film_work.description,
        ARRAY_AGG(DISTINCT person.full_name)
        FILTER(WHERE person_film_work.role = 'director') AS director,
        ARRAY_AGG(DISTINCT person.full_name)
        FILTER(WHERE person_film_work.role = 'actor') AS actors_names,
        ARRAY_AGG(DISTINCT person.full_name)
        FILTER(WHERE person_film_work.role = 'writer') AS writers_names,
        JSON_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name))
        FILTER(WHERE person_film_work.role = 'actor') AS actors,
        JSON_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name))
        FILTER(WHERE person_film_work.role = 'writer') AS writers
        FROM film_work
        LEFT OUTER JOIN genre_film_work ON (film_work.id = genre_film_work.film_work_id)
        LEFT OUTER JOIN genre ON (genre_film_work.genre_id = genre.id)
        LEFT OUTER JOIN person_film_work ON (film_work.id = person_film_work.film_work_id)
        LEFT OUTER JOIN person ON (person_film_work.person_id = person.id)
        GROUP BY film_work.id, film_work.title, film_work.description, film_work.rating
        """)
        row = cursor.fetchall()
        set_set_last_change_date()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()

