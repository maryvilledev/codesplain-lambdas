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

    def run_tests (self):
        print '\nTesting /users/{{user_id}}/snippets/{{snippet_id}} Endpoint:'
        self.test_options()
        self.test_get()
        self.test_put('to existing snippet_id')
        self.test_delete()
        self.test_put('to a new snippet_id')
        self.test_put_no_token()
        self.test_put_invalid_token()
        # Add test for invalid {{snippet_id}} when
        # https://github.com/maryvilledev/codesplain-lambdas/issues/88
        # is resolved.

        # Cleanup
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        r = requests.delete(self.API_URL, headers=headers, data=self.SNIPPET)

    def test_options (self):
        """Validate OPTIONS response"""
        print('\tTesting OPTIONS method')
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
            'GET,PUT,DELETE'
        )
        self.assertEqual(
            r.headers['Access-Control-Allow-Origin'],
            '*'
        )

        print '\t\tBody should be empty'
        self.assertEqual(r.text, '')

    def test_get (self):
        """GET a JSON snippet"""
        print '\tTesting GET method'
        r = requests.get(self.API_URL)

        print '\t\tStatus code should be 200'
        self.assertEqual(r.status_code, 200)

        print '\t\tBody should be valid JSON'
        try:
            body_json = r.json()
        except ValueError as error:
            self.fail('Body is not valid JSON')

        print '\t\tResponse body should == snippet (from config file)'
        self.assertEqual(body_json, json.loads(self.SNIPPET))

    def test_put (self, note):
        """PUT to a {{snippet_id}}"""
        print '\tTesting PUT method (' + note + ')'
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        r = requests.put(self.API_URL, headers=headers, data=self.SNIPPET)

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

    def test_delete (self):
        """DELETE a snippet"""
        print '\tTesting DELETE method'
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        r = requests.delete(self.API_URL, headers=headers, data=self.SNIPPET)

        print '\t\tResponse code is 200'
        self.assertEqual(r.status_code, 200)

        print '\t\tCORS header are present'
        self.assertEqual(r.headers['Access-Control-Allow-Origin'], '*')

        print '\t\tBody is valid JSON'
        try:
            body_json = r.json()
        except ValueError as error:
            self.fail('Body is not valid JSON')

        print '\t\tBody contains "response" and "response" is correct'
        try:
            self.assertEqual(body_json['response'], 'Successfully deleted.')
        except KeyError as error:
            self.fail('"response" does not exit in response')

    def test_put_no_token (self):
        print '\tTesting PUT method (with no auth token)'
        r = requests.put(self.API_URL, data=self.SNIPPET)

        print '\t\tResponse code is 401'
        self.assertEqual(r.status_code, 401)

        print '\t\tBody is valid JSON'
        try:
            body_json = r.json()
        except ValueError as error:
            self.fail('Body is not valid JSON')

        print '\t\tBody contains "message" and "message" is correct'
        try:
            self.assertEqual(body_json['message'], 'Unauthorized')
        except KeyError as error:
            self.fail('"message" does not exist in response')

    def test_put_invalid_token (self):
        print '\tTesting PUT method (with invalid auth token)'
        headers = { 'Authorization' : 'vim is the best editor' }
        r = requests.put(self.API_URL, headers=headers, data=self.SNIPPET)

        print '\t\tResponse code is 401'
        self.assertEqual(r.status_code, 401)

        print '\t\tBody is valid JSON'
        try:
            body_json = r.json()
        except ValueError as error:
            self.fail('Body is not valid JSON')

        print '\t\tBody contains "message" and "message" is correct'
        try:
            self.assertEqual(body_json['message'], 'Unauthorized')
        except KeyError as error:
            self.fail('"message" does not exist in response')
