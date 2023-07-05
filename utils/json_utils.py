"""JSON file handling utilities"""
import json


def read_json_file(path):
    """Used to read a json file"""
    with open(path) as f:
        data = json.load(f)
    return data
