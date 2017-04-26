import unittest
import requests
import json
import config

class TestEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass (cls):
        config_dict  = config.parse()
        cls.API_URL = config_dict['url'] + '/auth'

    def run_tests (self):
        print '\nTesting /auth endpoint:'
        self.test_options()
        self.test_post_invalid_code()

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

    def test_post_invalid_code (self):
        print '\tTesting POST method (with no auth code)'
        body = json.dumps({ 'code' : 'vim is a (nifty) text editor' })
        r = requests.post(self.API_URL, data=body)

        print '\t\tStatus code should be 400'
        self.assertEqual(r.status_code, 400)

        print '\t\tCORS headers are present'
        self.assertEqual(
            r.headers['Access-Control-Allow-Origin'],
            '*'
        )

        print '\t\tBody  is correct'
        self.assertEqual(r.text, 'The authorization code is invalid')
