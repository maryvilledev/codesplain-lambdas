import unittest
import json
import requests

class TestEndpoint(unittest.TestCase):
    global API_URL
    API_URL = 'https://api.codesplain.io/sandbox/users/Hopding/snippets'

    def test_response (self):
        """Validate OPTIONS response"""
        r = requests.options(API_URL)

        # Status code should be 200
        self.assertEqual(r.status_code, 200)

        # CORS headers should be present
        self.assertEqual(
            r.headers['Access-Control-Allow-Headers'],
            'Content-Type,X-Amz-Date,Authorization,x-api-key,x-amz-security-token'
        )
        self.assertEqual(
            r.headers['Access-Control-Allow-Methods'],
            'GET, POST'
        )
        self.assertEqual(
            r.headers['Access-Control-Allow-Origin'],
            '*'
        )

        # Body should be empty
        self.assertEqual(r.text, '')
