import json
from dataclass import Movie


def create_dataclass_list(data):
    body = []
    for row in data:
        data_template = Movie(
            id=row[0],
            imdb_rating=row[1],
            genre=row[2],
            title=row[3],
            description=row[4],
            director=row[5],
            actors_names=row[6],
            writers_names=row[7],
            actors=row[8],
            writers=row[9]
        )
        body.append(data_template)
    return body


def create_data_to_elastic(dataclass_list):
    with open('data/data_file.json', 'w') as f:
        body = []
        for row in dataclass_list:
            index_template = {"index": {"_index": "movies", "_id": str(row.id)}}
            data_template = {
                "id": str(row.id),
                "imdb_rating": row.imdb_rating,
                "genre": row.genre,
                "title": row.title,
                "description": row.description,
                "director": row.director,
                "actors_names": row.actors_names,
                "writers_names": row.writers_names,
                "actors": row.actors,
                "writers": row.writers,
                }
            body.append(index_template)
            body.append(data_template)
        json.dump(body, f, indent=4)
