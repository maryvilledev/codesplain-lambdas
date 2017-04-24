import unittest
import json
import requests
from jsonschema import validate, ValidationError
import config

class TestEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass (self):
        config_dict       = config.parse()
        self.USER_ID      = config_dict['user_id']
        self.API_URL      = config_dict['url'] + '/users/' + self.USER_ID + '/snippets'
        self.ACCESS_TOKEN = config_dict['access_token']
        self.SNIPPET      = json.dumps(config_dict['snippet'])

    def run_tests (self):
        print '\nTesting /users/{{user_id}}/snippets Endpoint:'
        self.test_options()
        self.test_post()
        self.test_get()

    def test_options (self):
        """Validate OPTIONS response"""
        print '\tTesting OPTIONS method'
        r = requests.options(self.API_URL)

        print '\t\tStatus code should be 200'
        self.assertEqual(r.status_code, 200)

        print '\t\tCORS headers should be present'
        self.assertEqual(
            r.headers['Access-Control-Allow-Headers'],
            'Content-Type,X-Amz-Date,Authorization,x-api-key,x-amz-security-token'
        )
        self.assertEqual(
            r.headers['Access-Control-Allow-Methods'],
            'GET, POST'
        )
        self.assertEqual(
            r.headers['Access-Control-Allow-Origin'],
            '*'
        )

        print '\t\tBody should be empty'
        self.assertEqual(r.text, '')


    def test_get (self):
        """GET user's index.json file"""
        print '\tTesting GET method'
        r = requests.get(self.API_URL)

        print '\t\tStatus code should be 200'
        self.assertEqual(r.status_code, 200)

        print '\t\tBody should be valid JSON'
        try:
            body_json = r.json()
        except ValueError as error:
            self.fail('Body is not valid JSON')

        print '\t\tBody object keys should be valid snippet meta data'
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
        for key, value in body_json.items():
            try:
                validate(body_json[key], schema)
            except ValidationError as error:
                self.fail("Body object keys not valid snippet meta data")
                print error

    def test_post (self):
        """POST a JSON snippet"""
        print '\tTesting POST method'
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        r = requests.post(self.API_URL, headers=headers, data=self.SNIPPET)

        print '\t\tResponse code is 200'
        self.assertEqual(r.status_code, 200)

        print '\t\tCORS headers are present'
        self.assertEqual(r.headers['Access-Control-Allow-Origin'], '*')

        print '\t\tBody is valid JSON'
        try:
            body_json = r.json()
        except ValueError as error:
            self.fail('Body is not valid JSON')

        print '\t\tBody contains "key" and "key" is correct'
        try:
            # Received "key" should equal expected "key", up
            # until possible postfix
            snippet_dict = json.loads(self.SNIPPET)
            expected_key = snippet_dict['snippetTitle'].replace(' ', '_').lower()
            self.assertEqual(
                body_json['key'][0:len(expected_key)],
                expected_key
            )
        except KeyError as error:
            self.fail('"key" does not exist in response')

        # Update config file with received key for later tests
        config.update('snippet_id', body_json['key'])
