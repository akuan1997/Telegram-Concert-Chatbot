import json


def read_json(json_filename):
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
