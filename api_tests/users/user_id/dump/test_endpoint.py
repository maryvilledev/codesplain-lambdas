import unittest
import json
import requests
from jsonschema import validate, ValidationError
import config
import testfor
from urlparse import urlparse

class TestEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass (cls):
        config_dict       = config.parse()
        cls.USER_ID      = config_dict['user_id']
        cls.API_URL      = config_dict['url'] + '/users/' + cls.USER_ID + '/dump'
        cls.ACCESS_TOKEN = config_dict['access_token']
        cls.SNIPPET      = json.dumps(config_dict['snippet'])

    def run_tests (self):
        print '\nTesting /users/{{user_id}}/dump Endpoint:'
        self.test_options()
        self.test_post()

    def test_options (self):
        print '\tTesting OPTIONS method'
        r = requests.options(self.API_URL)

        testfor.status_code(self, r, 200)
        testfor.cors_headers(self, r, {
            'Headers' : 'Content-Type,X-Amz-Date,Authorization,x-api-key,x-amz-security-token',
            'Methods' : 'POST',
            'Origin'  : '*'
        })
        testfor.body(self, r, '')

    def test_post (self):
        print '\tTesting POST method'
        r = requests.post(self.API_URL)

        testfor.status_code(self, r, 200)
        testfor.cors_headers(self, r, { 'Origin' : '*' })
        p = urlparse(r.text)
        if p.scheme != 'https' or self.USER_ID + '/snippets.zip' not in p.path:
            self.fail('Response is not URL or is incorrect')
