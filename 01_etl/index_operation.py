import os
import elasticsearch
from utils import backoff
from config import config, logger

path = os.path.abspath('index/index_schema.json')


@backoff()
def create_index():
    with open(path, 'r') as file:
        data = file.read()
        es = elasticsearch.Elasticsearch([config], request_timeout=300)
        try:
            es.indices.create(index='movies', body=data)
            logger.info('Создание индекса завершено')
        except elasticsearch.exceptions.RequestError as ex:
            if ex.error == 'resource_already_exists_exception':
                pass
            else:
                raise ex
