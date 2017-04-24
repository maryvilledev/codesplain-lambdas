import unittest
import requests
import config

class TestEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass (self):
        config_dict  = config.parse()
        self.API_URL = config_dict['url'] + '/parsers/'

    def run_tests (self):
        print '\nTesting /parsers{{language}} Endpoint:'
        self.test_options('python3')
        self.test_get('python3')
        self.test_options('java8')
        self.test_get('java8')

    def test_options (self, language):
        print '\tTesting OPTIONS method (for ' + language + ')'
        r = requests.options(self.API_URL + language)

        print '\t\tStatus code should be 200'
        self.assertEqual(r.status_code, 200)

        print '\t\tCORS headers should be present'
        self.assertEqual(
            r.headers['Access-Control-Allow-Headers'],
            'Content-Type,X-Amz-Date,Authorization,x-api-key,x-amz-security-token'
        )
        self.assertEqual(
            r.headers['Access-Control-Allow-Methods'],
            'GET'
        )
        self.assertEqual(
            r.headers['Access-Control-Allow-Origin'],
            '*'
        )

        print '\t\tBody should be empty'
        self.assertEqual(r.text, '')

    def test_get (self, language):
        print '\tTesting GET method (for ' + language + ')'
        r = requests.get(self.API_URL + language)

        print '\t\tStatus code should be 200'
        self.assertEqual(r.status_code, 200)

        print '\t\tResponse could be a valid parser'
        # Make sure we get a response that could actually be
        # a valid parser. 100000 is a guesstimate
        self.assertTrue(len(r.text) >= 100000)
