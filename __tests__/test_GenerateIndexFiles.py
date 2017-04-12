import sys
import os
import unittest
from mock import patch

os.environ['BucketName'] = 'mockBucketName'
import lambdas.GenerateIndexFiles.lambda_function as gif

class TestGenerateIndexFiles(unittest.TestCase):
    def setUp (self):
        ## We're going to mock out some global functions, so re-import before each
        reload(gif)

    def test_has_index (self):
        """Should return True iff 'index.json' is a file"""
        self.assertTrue(gif.has_index(['index.json']))
        self.assertFalse(gif.has_index([]))

    @patch('lambdas.GenerateIndexFiles.lambda_function.get_snippet_info',
     return_value='mockSnippetInfo')
    def test_create_index (self, mock_fn):
        """Should create an index object"""
        mock_filenames = ['leet']
        mock_dir = 'hacks'
        mock_snippet_info = 'mockSnippetInfo'
        expected = {'hacks/leet': mock_snippet_info}
        self.assertEqual(gif.create_index(mock_dir, mock_filenames), expected)
        mock_fn.assert_called_once_with('hacks/leet')
