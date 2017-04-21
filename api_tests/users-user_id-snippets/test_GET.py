import unittest
import json
import requests
from jsonschema import validate
from jsonschema import ValidationError

class TestEndpoint(unittest.TestCase):
    global API_URL
    API_URL = 'https://api.codesplain.io/sandbox/users/Hopding/snippets'

    def test_get_index_file (self):
        """GET user's index.json file"""
        r = requests.get(API_URL)

        # Status code should be 200
        self.assertEqual(r.status_code, 200)

        # Body should be valid JSON
        try:
            bodyJson = r.json()
        except ValueError as error:
            self.fail("Body is not valid JSON")

        # Body object keys should be valid snippet meta data
        schema = {
            'title'      : 'Snippet Meta Data',
            'type'       : 'object',
            'properties' : {
                'snippetTitle' : {'type' : 'string'},
                'language'     : {'type' : 'string'},
                'lastEdited'   : {'type' : 'string'},
            },
            'required' : ['snippetTitle', 'language', 'lastEdited'],
        }
        for key, value in bodyJson.items():
            try:
                validate(bodyJson[key], schema)
            except ValidationError as error:
                self.fail("Body object keys not valid snippet meta data")
                print error
