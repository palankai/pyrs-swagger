import json
import os

import jsonschema


def validate(data):
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'schema.json'), 'r') as schemafile:
        schema = json.load(schemafile)
    jsonschema.validate(data, schema)
