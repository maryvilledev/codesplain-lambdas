import unittest
import json
import requests
from os.path import dirname, abspath

class TestEndpoint(unittest.TestCase):
    API_URL    = None
    SNIPPET_ID = None
    USER_ID    = None

    @classmethod
    def setUpClass (self):
        # Parse config file and initialize class vars
        # dirname() walks up tree, abspath(__file__) is dir of this script
        config_path = dirname(dirname(abspath(__file__))) + '/config.json'
        config_dict = json.load(open(config_path, 'r'))
        self.USER_ID = config_dict['user_id']
        self.SNIPPET_ID = config_dict['snippet_id']
        self.API_URL = config_dict['url'] + '/users/' + self.USER_ID + '/snippets/' + self.SNIPPET_ID

    def test_response (self):
        """Validate OPTIONS response"""
        r = requests.options(self.API_URL)

        # Status code should be 200
        self.assertEqual(r.status_code, 200)

        # CORS headers should be present
        self.assertEqual(
            r.headers['Access-Control-Allow-Headers'],
            'Content-Type,X-Amz-Date,Authorization,x-api-key,x-amz-security-token'
        )
        self.assertEqual(
            r.headers['Access-Control-Allow-Methods'],
            'GET,PUT,DELETE'
        )
        self.assertEqual(
            r.headers['Access-Control-Allow-Origin'],
            '*'
        )

        # Body should be empty
        self.assertEqual(r.text, '')
