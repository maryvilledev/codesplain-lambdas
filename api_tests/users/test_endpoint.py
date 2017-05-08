import unittest
import json
import requests
from jsonschema import validate, ValidationError
import config
import testfor

class TestEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass (cls):
        config_dict      = config.parse()
        cls.USER_ID      = config_dict['user_id']
        cls.SNIPPET_ID   = config_dict['snippet_id']
        cls.API_URL      = config_dict['url'] + '/users'
        cls.ACCESS_TOKEN = config_dict['access_token']
        cls.SNIPPET      = json.dumps(config_dict['snippet'])

    def run_tests (self):
        print '\nTesting /users Endpoint:'
        self.test_options()
        self.test_get_no_query()
        self.test_get_with_query()

    def test_options (self):
        print('\tTesting OPTIONS method')
        r = requests.options(self.API_URL)

        testfor.status_code(self, r, 200)
        testfor.cors_headers(self, r, {
            'Headers' : 'Content-Type,X-Amz-Date,Authorization,x-api-key,x-amz-security-token',
            'Methods' : 'GET,OPTIONS',
            'Origin'  : '*'
        })
        testfor.body(self, r, '')

    def test_get_no_query (self):
        print '\tTesting GET method (with no query string)'
        r = requests.get(self.API_URL)

        testfor.status_code(self, r, 200)
        testfor.valid_json(self, r)

        print '\t\tBody object keys should be valid index entries'
        schema = {
            'title'      : 'Index Entry',
            'type'       : 'object',
            'properties' : {
                'lastEdited'   : {'type' : 'string'},
                'language'     : {'type' : 'string'},
                'snippetTitle' : {'type' : 'string'},
            },
            'required': ['lastEdited', 'language', 'snippetTitle'],
        }
        for user, index in r.json().items():
            for snippet, entry in index.items():
                try:
                    validate(entry, schema)
                except ValidationError as error:
                    self.fail('Found invalid index entry')

    def test_get_with_query (self):
        print '\tTesting GET method (with query string)'
        url = self.API_URL + "?users=" + self.USER_ID
        r = requests.get(url)

        testfor.status_code(self, r, 200)
        testfor.valid_json(self, r)

        print '\t\tBody object keys should be valid index entries'
        schema = {
            'title'      : 'Index Entry',
            'type'       : 'object',
            'properties' : {
                'lastEdited'   : {'type' : 'string'},
                'language'     : {'type' : 'string'},
                'snippetTitle' : {'type' : 'string'},
            },
            'required': ['lastEdited', 'language', 'snippetTitle'],
        }
        index = r.json()[self.USER_ID].items()
        for snippet, entry in index:
            try:
                validate(entry, schema)
            except ValidationError as error:
                self.fail('Found invalid index entry')
