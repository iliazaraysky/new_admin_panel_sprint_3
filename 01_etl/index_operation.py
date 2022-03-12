import os
import elasticsearch

path = os.path.abspath('index/index_schema.json')


def create_index(config):
    with open(path, 'r') as file:
        data = file.read()
        es = elasticsearch.Elasticsearch([config], request_timeout=300)
        try:
            es.indices.create(index='movies', body=data)
        except elasticsearch.exceptions.RequestError as ex:
            if ex.error == 'resource_already_exists_exception':
                pass
            else:
                raise ex
