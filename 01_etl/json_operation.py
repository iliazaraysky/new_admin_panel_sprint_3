import json
import uuid
import requests


def generate_json_file(api_url):
    with open('data.json', 'w') as f:
        response = requests.get(api_url)
        data_from_api = response.json()
        body = []

        for obj in data_from_api['results']:
            index_template = {"index": {"_index": "movies", "_id": str(uuid.uuid4())}}
            data_template = {
                "id": obj['id'],
                "imdb_rating": obj['rating'],
                "genre": obj['genres'],
                "title": obj['title'],
                "description": obj['description'],
                "director": obj['directors'],
                "actors_names": obj['actors'],
                "writers_names": obj['writers'],
                "actors": list(),
                "writers": list(),
                }

            for id, name in zip(obj['actors_id'],
                                obj['actors']):
                persons_template = {'id': id, 'name': name}
                data_template['actors'].append(persons_template)

            for id, name in zip(obj['writers_id'],
                                obj['writers']):
                persons_template = {'id': id, 'name': name}
                data_template['writers'].append(persons_template)

            body.append(index_template)
            body.append(data_template)
        json.dump(body, f, indent=4)
