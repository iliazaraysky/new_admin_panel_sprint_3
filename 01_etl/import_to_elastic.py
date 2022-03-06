import json


def bulk_data_to_elastic(file):
    with open(file) as json_file:
        data = json.load(json_file)
        return data
