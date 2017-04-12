import sys
import os
import unittest

from lambdas.GenerateIndexFiles import *

class TestGenerateIndexFiles(unittest.TestCase):
    def test_has_index (self):
        """Should return True iff 'index.json' is a file"""
        self.assertTrue(has_index(['index.json']))
        self.assertFalse(has_index([]))
