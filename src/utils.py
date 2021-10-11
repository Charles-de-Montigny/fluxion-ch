import json


def read_json(input_path: str):
    """
    Convert a JSON string to dictionnary.
    """
    with open(input_path) as file:
        data = json.load(file)
    return data