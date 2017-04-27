import unittest
import requests
import config

class TestEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass (cls):
        config_dict  = config.parse()
        cls.API_URL = config_dict['url'] + '/mappings/'

    def run_tests (self):
        print '\nTesting /mappings/{{language}} Endpoint:'
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

        print '\t\tResponse is valid csv'
        csv_lines  = r.text.split('\n')
        num_commas = csv_lines[0].count(',')
        for line in csv_lines[0:-2]: # ignore newline at the end
            if line.count(',') != num_commas:
                self.fail('Response is not valid csv.')
