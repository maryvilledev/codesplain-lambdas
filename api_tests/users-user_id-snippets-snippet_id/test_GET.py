import unittest
import json
import requests
from os.path import dirname, abspath

class TestEndpoint(unittest.TestCase):
    API_URL    = None
    SNIPPET_ID = None
    USER_ID    = None
    SNIPPET    = None

    @classmethod
    def setUpClass (self):
        # Parse config file and initialize class vars
        # dirname() walks up tree, abspath(__file__) is dir of this script
        config_path = dirname(dirname(abspath(__file__))) + '/config.json'
        config_dict = json.load(open(config_path, 'r'))
        self.USER_ID = config_dict['user_id']
        self.SNIPPET_ID = config_dict['snippet_id']
        self.API_URL = config_dict['url'] + '/users/' + self.USER_ID + '/snippets/' + self.SNIPPET_ID
        self.SNIPPET = json.dumps(config_dict['snippet'])

    def test_get_snippet (self):
        """GET a JSON snippet"""
        r = requests.get(self.API_URL)

        # Status code should be 200
        self.assertEqual(r.status_code, 200)

        # Body should be valid JSON
        try:
            body_json = r.json()
        except ValueError as error:
            self.fail('Body is not valid JSON')

        # Body == snippet (from config file)
        self.assertEqual(body_json, json.loads(self.SNIPPET))
