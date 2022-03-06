from elasticsearch import Elasticsearch
from index_operation import create_index
from test_bug_fix import fix_data
from import_to_elastic import bulk_data_to_elastic
from json_operation import generate_json_file


api_url = 'http://127.0.0.1:8000/api/v1/movies/'
config = {
    'scheme': 'http',
    'host': '127.0.0.1',
    'port': 9200
}
es = Elasticsearch([config], request_timeout=300)

if __name__ == '__main__':
    create_index(config)    # Создаест индекс
    generate_json_file(api_url) # Создаст локальный файл 'data.json'
    fix_data('data.json')   # Исправит ошибку для прохождения тестов
    bulk_data_to_elastic('data.json')   # Загрузка данных в Elasticsearch

    es.bulk(index='movies', body=bulk_data_to_elastic('data.json'))
