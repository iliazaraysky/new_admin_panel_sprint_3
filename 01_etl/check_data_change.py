import os
import json
import logging
import datetime
import psycopg2
from dotenv import load_dotenv

log_folder = os.path.abspath('logs')
log_name = 'check_data_change.log'
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


def set_set_last_change_date():
    body = []
    with open('./modify/modify.json', 'w') as f:
        now = datetime.datetime.now()
        data_template = {
            "last_modify": now.strftime("%Y-%m-%d %H:%M:%S")
        }
        body.append(data_template)
        json.dump(body, f, indent=4)


def load_last_mod():
    try:
        with open('./modify/modify.json', 'r') as f:
            data = json.load(f)
            return data[0]['last_modify']
    except FileNotFoundError:
        print('File not found')


def check_change(dsl):
    conn = psycopg2.connect(**dsl)
    cursor = conn.cursor()
    last_mod = load_last_mod()
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
        FILTER(WHERE person_film_work.role = 'writer') AS writers,
        film_work.modified
        FROM film_work
        LEFT OUTER JOIN genre_film_work ON (film_work.id = genre_film_work.film_work_id)
        LEFT OUTER JOIN genre ON (genre_film_work.genre_id = genre.id)
        LEFT OUTER JOIN person_film_work ON (film_work.id = person_film_work.film_work_id)
        LEFT OUTER JOIN person ON (person_film_work.person_id = person.id)
        WHERE film_work.modified > '%s'
        GROUP BY film_work.id, film_work.title, film_work.description, film_work.rating
        """ % last_mod)
        row = cursor.fetchall()
        set_set_last_change_date()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
