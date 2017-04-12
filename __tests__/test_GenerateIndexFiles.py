import sys
import os
import unittest
from mock import Mock, patch

sys.modules['boto3'] = Mock()
os.environ['BUCKET_NAME'] = 'mockBucketName'
import lambdas.GenerateIndexFiles as gif

class TestGenerateIndexFiles(unittest.TestCase):
    def setUp (self):
        ## We're going to mock out some global functions, so re-import before each
        reload(gif)

    def test_has_index (self):
        """Should return True iff 'index.json' is a file"""
        self.assertTrue(gif.has_index(['index.json']))
        self.assertFalse(gif.has_index([]))

    def test_create_index (self):
        """Should create an index object"""
        mock_filenames = ['leet']
        mock_dir = 'hacks'
        mock_snippet_info = 'mockSnippetInfo'
        gif.get_snippet_info = Mock(return_value=mock_snippet_info)
        expected = {'hacks/leet': mock_snippet_info}
        self.assertEqual(gif.create_index(mock_dir, mock_filenames), expected)
