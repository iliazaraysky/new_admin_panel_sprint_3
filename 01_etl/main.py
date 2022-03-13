import os.path
import datetime
import elasticsearch
from config import config, logger
from utils import backoff
from index_operation import create_index
from import_to_elastic import bulk_data_to_elastic
from postgres_extract import retrieve_data_from_postgres
from check_data_change import check_change, load_last_mod
from json_operation import create_dataclass_list, create_data_to_elastic


@backoff()
def main():
    if os.path.exists('./modify/modify.json'):
        try:
            now = datetime.datetime.now()
            time_to_check = now + datetime.timedelta(minutes=1)
            if time_to_check.strftime("%Y-%m-%d %H:%M:%S") > load_last_mod():
                create_data_to_elastic(
                    create_dataclass_list(
                        check_change()
                    )
                )
                return es.bulk(index='movies', body=bulk_data_to_elastic('data/data_file.json'))
        except ValueError as error:
            logger.error(error)
    else:
        create_index()
        create_data_to_elastic(
            create_dataclass_list(
                retrieve_data_from_postgres()
            )
        )
        return es.bulk(index='movies', body=bulk_data_to_elastic('data/data_file.json'))


if __name__ == '__main__':
    if not os.path.exists('./data'):
        os.makedirs('./data')

    if not os.path.exists('./modify'):
        os.makedirs('./modify')

    es = elasticsearch.Elasticsearch([config], request_timeout=300)

    main()
