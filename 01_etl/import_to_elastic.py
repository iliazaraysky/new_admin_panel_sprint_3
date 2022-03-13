import json
from config import logger


def bulk_data_to_elastic(file):
    with open(file) as json_file:
        data = json.load(json_file)
        logger.info('Импорт данных в ES завершен')
        return data
