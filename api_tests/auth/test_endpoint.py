import unittest
import requests
import config

class TestEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass (self):
        config_dict  = config.parse()
        self.API_URL = config_dict['url'] + '/auth'

    def run_tests (self):
        print '\nTesting /auth Endpoint:'
        self.test_options()

    def test_options (self):
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
            'POST'
        )
        self.assertEqual(
            r.headers['Access-Control-Allow-Origin'],
            '*'
        )

        print '\t\tBody should be empty'
        self.assertEqual(r.text, '')
