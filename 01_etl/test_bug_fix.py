import json

file = 'data.json'


def fix_data(file):
    with open(file, 'r+') as json_file:
        data = json.load(json_file)
        for row in data:
            try:
                if row['id'] == '68dfb5e2-7014-4738-a2da-c65bd41f5af5':
                    row['writers_names'].append('William A. Wellman')
                    json_file.seek(0)
                    json.dump(data, json_file, indent=4)
                    json_file.truncate()
            except KeyError:
                pass
    json_file.close()
