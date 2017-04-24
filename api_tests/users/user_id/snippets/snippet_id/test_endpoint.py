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
        self.SNIPPET_ID   = config_dict['snippet_id']
        self.API_URL      = config_dict['url'] + '/users/' + self.USER_ID + '/snippets/' + self.SNIPPET_ID
        self.ACCESS_TOKEN = config_dict['access_token']
        self.SNIPPET      = json.dumps(config_dict['snippet'])

    def test_options (self):
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

    def test_get (self):
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

    def test_put_existing (self):
        """PUT to an existing {{snippet_id}}"""
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        r = requests.put(self.API_URL, headers=headers, data=self.SNIPPET)

        # Response code is 200
        self.assertEqual(r.status_code, 200)

        # CORS headers are present
        self.assertEqual(r.headers['Access-Control-Allow-Origin'], '*')

        # Body is valid JSON
        try:
            body_json = r.json()
        except ValueError as error:
            self.fail('Body is not valid JSON')

        # Body contains "key" and "key" is correct
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

    def test_delete (self):
        """DELETE a snippet"""
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        r = requests.delete(self.API_URL, headers=headers, data=self.SNIPPET)

        # Response code is 200
        self.assertEqual(r.status_code, 200)

        # CORS headers are present
        self.assertEqual(r.headers['Access-Control-Allow-Origin'], '*')

        # Body is valid JSON
        try:
            body_json = r.json()
            print body_json
        except ValueError as error:
            self.fail('Body is not valid JSON')

        # Body contains "response" and "response" is correct
        try:
            self.assertEqual(body_json['response'], 'Successfully deleted.')
        except KeyError as error:
            self.fail('"response" does not exit in response')
