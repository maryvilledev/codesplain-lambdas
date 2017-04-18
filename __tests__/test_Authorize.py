import sys
import os
import unittest
from mock import patch, Mock

with patch('boto3.client'):
    os.environ['ClientID'] = 'MockClientId'
    os.environ['ClientSecret']= 'FooBar'
    import lambdas.Authorize.lambda_function as auth

class TestAuthorize(unittest.TestCase):
    @patch('boto3.client')
    def setUp (self, mock_boto3):
        ## We're going to mock out some global functions, so re-import before each
        reload(auth)
        ## Mock out the s3 object
        auth.s3 = Mock()

    @patch('requests.get')
    def test_auth_request(self, mock_requests):
        mock_client_id = 'Thing1'
        mock_client_secret = 'Thing2'
        mock_token = '123'

        auth.auth_request(mock_client_id, mock_client_secret, mock_token)

        mock_requests.assert_called_once_with('https://api.github.com/applications/%s/tokens/%s' % (mock_client_id, mock_token), auth=(mock_client_id, mock_client_secret))
