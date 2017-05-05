import unittest
import json
import requests
from jsonschema import validate, ValidationError
import config
import testfor

class TestEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass (cls):
        config_dict       = config.parse()
        cls.USER_ID      = config_dict['user_id']
        cls.SNIPPET_ID   = config_dict['snippet_id']
        cls.API_URL      = config_dict['url'] + '/users/' + cls.USER_ID + '/snippets/' + cls.SNIPPET_ID
        cls.INVALID_SNIPPET_KEY = config_dict['invalid_snippet_key']
        cls.INVALID_SNIPPET_URL = '%s/users/%s/snippets/%s' % (config_dict['url'], cls.USER_ID, cls.INVALID_SNIPPET_KEY) 
        cls.ACCESS_TOKEN = config_dict['access_token']
        cls.SNIPPET      = json.dumps(config_dict['snippet'])

    def run_tests (self):
        print '\nTesting /users/{{user_id}}/snippets/{{snippet_id}} Endpoint:'
        self.test_options()
        self.test_get()
        self.test_get_invalid_snippet()
        self.test_put('to existing snippet_id')
        self.test_delete()
        self.test_put('to a new snippet_id')
        self.test_put_no_token()
        self.test_put_invalid_token()

        # Cleanup
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        r = requests.delete(self.API_URL, headers=headers, data=self.SNIPPET)

    def test_options (self):
        print('\tTesting OPTIONS method')
        r = requests.options(self.API_URL)

        testfor.status_code(self, r, 200)
        testfor.cors_headers(self, r, {
            'Headers' : 'Content-Type,X-Amz-Date,Authorization,x-api-key,x-amz-security-token',
            'Methods' : 'GET,PUT,DELETE',
            'Origin'  : '*'
        })
        testfor.body(self, r, '')

    def test_get (self):
        print '\tTesting GET method'
        r = requests.get(self.API_URL)

        testfor.status_code(self, r, 200)
        testfor.valid_json(self, r)
        testfor.body(self, r, self.SNIPPET)

    def test_get_invalid_snippet(self):
        print '\tTesting GET method (with invalid snippet id)'
        r = requests.get(self.INVALID_SNIPPET_URL)

        testfor.status_code(self, r, 404)
        testfor.cors_headers(self, r, {'Origin': '*'})
        testfor.body(self, r, 'No snippet exists with key "%s/%s"' % (TestEndpoint.USER_ID, TestEndpoint.INVALID_SNIPPET_KEY))
    

    def test_put (self, note):
        print '\tTesting PUT method (' + note + ')'
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        r = requests.put(self.API_URL, headers=headers, data=self.SNIPPET)

        testfor.status_code(self, r, 200)
        testfor.cors_headers(self, r, { 'Origin' : '*' })
        testfor.valid_json(self, r)

        expected_key = json.loads(self.SNIPPET) \
                           ['snippetTitle']     \
                           .replace(' ', '_')   \
                           .lower()
        testfor.key_val_start(self, r, 'key', expected_key)

    def test_delete (self):
        print '\tTesting DELETE method'
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        r = requests.delete(self.API_URL, headers=headers, data=self.SNIPPET)

        testfor.status_code(self, r, 200)
        testfor.cors_headers(self, r, { 'Origin' : '*' })
        testfor.valid_json(self, r)
        testfor.key_val(self, r, 'response', 'Successfully deleted.')

    def test_put_no_token (self):
        print '\tTesting PUT method (with no auth token)'
        r = requests.put(self.API_URL, data=self.SNIPPET)

        testfor.status_code(self, r, 401)
        testfor.valid_json(self, r)
        testfor.key_val(self, r, 'message', 'Unauthorized')

    def test_put_invalid_token (self):
        print '\tTesting PUT method (with invalid auth token)'
        headers = { 'Authorization' : 'vim is the best editor' }
        r = requests.put(self.API_URL, headers=headers, data=self.SNIPPET)

        testfor.status_code(self, r, 401)
        testfor.valid_json(self, r)
        testfor.key_val(self, r, 'message', 'Unauthorized')
