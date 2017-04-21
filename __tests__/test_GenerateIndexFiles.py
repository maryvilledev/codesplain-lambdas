import sys
import os
import unittest
from mock import patch, Mock

os.environ['BucketName'] = 'mockBucketName'
import lambdas.GenerateIndexFiles.lambda_function as gif

class TestGenerateIndexFiles(unittest.TestCase):
    def setUp (self):
        ## We're going to mock out some global functions, so re-import before each
        reload(gif)
        ## Mock out the s3 object
        gif.s3 = Mock()

    def test_has_index (self):
        """Should return True if 'index.json' is a file"""
        self.assertTrue(gif.has_index(['index.json']))
        self.assertFalse(gif.has_index([]))

    def test_delete_index_file (self):
        """Should delete the existing index file"""
        mock_dir = 'hacks'
        gif.delete_index_file(mock_dir)
        gif.s3.Object.assert_called_once_with('mockBucketName', 'hacks/index.json')

    @patch('lambdas.GenerateIndexFiles.lambda_function.get_snippet_info',
     return_value='mockSnippetInfo')
    def test_create_index (self, mock_fn):
        """Should create an index object"""
        mock_filenames = ['leet']
        mock_dir = 'hacks'
        mock_snippet_info = 'mockSnippetInfo'
        expected = {'leet': mock_snippet_info}
        self.assertEqual(gif.create_index(mock_dir, mock_filenames), expected)
        mock_fn.assert_called_once_with('hacks/leet')
