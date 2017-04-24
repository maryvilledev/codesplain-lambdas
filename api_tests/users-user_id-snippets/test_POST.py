import unittest
import json
import requests
import os

class TestEndpoint(unittest.TestCase):
    API_URL      = None
    ACCESS_TOKEN = None
    SNIPPET_ID   = None
    USER_ID      = None
    SNIPPET      = None

    @classmethod
    def setUpClass (self):
        # Parse config file and initialize global vars
        config_path  = os.path.dirname(__file__) + '/config.json'
        config_dict  = json.load(open(config_path, 'r'))
        self.USER_ID      = config_dict['user_id']
        self.API_URL      = config_dict['url'] + '/users/' + self.USER_ID + '/snippets'
        self.ACCESS_TOKEN = config_dict['access_token']
        self.SNIPPET_ID   = config_dict['snippet_id']
        self.SNIPPET      = json.dumps(config_dict['snippet'])

    def test_save_snippet (self):
        """POST a JSON snippet"""
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        r = requests.post(self.API_URL, headers=headers, data=self.SNIPPET)

        # Reponse code is 200
        self.assertEqual(r.status_code, 200)

        # CORS headers are present
        self.assertEqual(r.headers['Access-Control-Allow-Origin'], '*')

        # Body is valid json
        try:
            bodyJson = r.json()
        except ValueError as error:
            self.fail('Body is not valid JSON')

        # Body contains "key" and "key" is correct
        try:
            # Received "key" should equal expected "key", up
            # until possible postfix
            snippet_dict = json.loads(self.SNIPPET)
            expected_key = snippet_dict['snippetTitle'].replace(' ', '_').lower()
            self.assertEqual(
                bodyJson['key'][0:len(expected_key)],
                expected_key
            )
        except KeyError as error:
            self.fail('"key" does not exist in response')
