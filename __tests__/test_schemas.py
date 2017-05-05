import unittest

from cerberus import Validator
from scripts.schema import snippet_schema

class TestSnippetSchema(unittest.TestCase):
    def setUp(self):
        self.validator = Validator(snippet_schema)

    def test_valid_snippet(self):
        """Should load a valid snippet dict with no errors"""
        snippet = {
            "annotations": {},
            "AST": {
                "begin": 0,
                "end": 1,
                "tags": [],
                "type": "",
                "children": [],
            },
            "filters": {},
            "readOnly": True,
            "snippet": "",
            "snippetLanguage": "",
            "snippetTitle": ""
        }
        self.validator.validate(snippet)
        self.assertEqual(len(self.validator.errors), 0)

    def test_invalid_snippet(self):
        """Should load an invalid snippet dict with errors"""
        snippet = {
            'snippet': [],
        }
        self.validator.validate(snippet)
        self.assertNotEqual(len(self.validator.errors), 0)
