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
        cls.API_URL      = config_dict['url'] + '/users/' + cls.USER_ID + '/snippets'
        cls.ACCESS_TOKEN = config_dict['access_token']
        cls.SNIPPET      = json.dumps(config_dict['snippet'])

    def run_tests (self):
        print '\nTesting /users/{{user_id}}/snippets Endpoint:'
        self.test_options()
        self.test_post()
        self.test_get()
        self.test_post_invalid_token()
        self.test_post_no_body()
        # TODO: when https://github.com/maryvilledev/codesplain-lambdas/issues/86
        # is resolved, add test for it.

    def test_options (self):
        print '\tTesting OPTIONS method'
        r = requests.options(self.API_URL)

        testfor.status_code(self, r, 200)
        testfor.cors_headers(self, r, {
            'Headers' : 'Content-Type,X-Amz-Date,Authorization,x-api-key,x-amz-security-token',
            'Methods' : 'GET, POST',
            'Origin'  : '*'
        })
        testfor.body(self, r, '')

    def test_get (self):
        print '\tTesting GET method'
        r = requests.get(self.API_URL)

        testfor.status_code(self, r, 200)
        testfor.valid_json(self, r)

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
        for key, value in r.json().items():
            try:
                validate(value, schema)
            except ValidationError as error:
                self.fail('Body object keys not valid snippet meta data')
                print error

    def test_post (self):
        print '\tTesting POST method'
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        r = requests.post(self.API_URL, headers=headers, data=self.SNIPPET)

        testfor.status_code(self, r, 200)
        testfor.cors_headers(self, r, {
            'Origin' : '*'
        })
        testfor.valid_json(self, r)

        expected_key = json.loads(self.SNIPPET) \
                           ['snippetTitle']     \
                           .replace(' ', '_')   \
                           .lower()
        testfor.key_val_start(self, r,'key', expected_key)

        # Update config file with received key for later tests
        config.update('snippet_id', r.json()['key'])

    def test_post_invalid_token (self):
        print '\tTesting POST method (with invalid auth token)'
        headers = { 'Authorization' : 'vim is the best editor' }
        r = requests.post(self.API_URL, headers=headers, data=self.SNIPPET)

        testfor.status_code(self, r, 401)
        testfor.valid_json(self, r)
        testfor.key_val(self, r, 'message', 'Unauthorized')

    def test_post_no_body (self):
        print '\tTesting POST method (with no body)'
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        r = requests.post(self.API_URL, headers=headers)

        testfor.status_code(self, r, 400)
        testfor.valid_json(self, r)
        testfor.key_val(self, r, 'message', 'Invalid request body')

    def test_post_no_title (self):
        print '\tTesting POSTT method (with no snippet title)'
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        data = {
            "snippetLanguage": "python3",
            "AST": {},
            "snippetTitle": "",
            "snippet": "",
            "readOnly": False,
            "filters": {},
            "annotations": {}
          }
        r = requests.post(self.API_URL, headers=headers, data=self.SNIPPET_NO_TITLE)

        testfor.status_code(self, r, 400)
        testfor.valid_json(self, r)
        testfor.key_val(self, r, 'message', 'Invalid request body')

    def test_post_invalid_language (self):
        print '\tTesting POSTT method (with invalid snippet language)'
        headers = { 'Authorization' : self.ACCESS_TOKEN }
        data = {
            "snippetLanguage": "python2",
            "AST": {},
            "snippetTitle": "title",
            "snippet": "",
            "readOnly": False,
            "filters": {},
            "annotations": {}
        }
        r = requests.post(self.API_URL, headers=headers, data=self.SNIPPET_INVALID_LANG)

        testfor.status_code(self, r, 400)
        testfor.valid_json(self, r)
        testfor.key_val(self, r, 'message', 'Invalid request body')
