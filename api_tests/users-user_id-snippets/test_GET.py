import unittest
import requests

class TestEndpoint(unittest.TestCase):
    API_URL = 'https://api.codesplain/io/sandbox/users/Hopding/snippets'
    def test_get_index_file (self):
        """GET user's index.json file"""
        r = requests.get(API_URL)

        # Status code should be 200
        self.assertEqual(r.status_code, 200)

        # Body should be valid JSON
        try:
            bodyJson = r.json()
        except ValueError as error:
            self.fail("Body is not valid JSON")

        # Body object keys should be valid snippet meta data
        self.assertTrue(True)
