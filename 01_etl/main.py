import os.path
import logging
import datetime
import elasticsearch
from dotenv import load_dotenv
from index_operation import create_index
from import_to_elastic import bulk_data_to_elastic
from postgres_extract import retrieve_data_from_postgres
from check_data_change import check_change, load_last_mod
from json_operation import create_dataclass_list, create_data_to_elastic

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


if __name__ == '__main__':
    dsl = {
        'dbname': os.getenv('POSTGRESQL_DB'),
        'user': os.getenv('POSTGRESQL_USER'),
        'password': os.getenv('POSTGRESQL_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

    config = {
        'scheme': os.getenv('SCHEME'),
        'host': os.getenv('DB_HOST_ELASTIC'),
        'port': os.getenv('ELASTIC_PORT')
    }

    es = elasticsearch.Elasticsearch([config], request_timeout=300)

    if os.path.exists('./modify/modify.json'):
        try:
            now = datetime.datetime.now()
            time_to_check = now + datetime.timedelta(minutes=1)
            if time_to_check.strftime("%Y-%m-%d %H:%M:%S") > load_last_mod():
                create_data_to_elastic(
                    create_dataclass_list(
                        check_change(dsl)
                    )
                )
                es.bulk(index='movies', body=bulk_data_to_elastic('data/data_file.json'))
        except ValueError:
            logging.error()
    else:
        create_index(config)
        create_data_to_elastic(
            create_dataclass_list(
                retrieve_data_from_postgres(dsl)
            )
        )
        es.bulk(index='movies', body=bulk_data_to_elastic('data/data_file.json'))
