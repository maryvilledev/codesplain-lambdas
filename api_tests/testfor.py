import json
import requests

# Verify that body is valid json, and return parsed dictionary
def valid_json(test_case, response):
    print '\t\tBody should be valid JSON'
    try:
        body_json = response.json()
    except ValueError as error:
        test_case.fail('Body is not valid JSON')

# Verify that the response has the given status code
def status_code(test_case, response, code):
    print '\t\tResonse code is ' + str(code)
    test_case.assertEqual(response.status_code, code)

# Verify that the response has the given "Access-Control-Allow-" headers
def cors_headers(test_case, response, dict):
    for key, value in dict.items():
        if key == 'Headers' or key == 'Access-Control-Allow-Headers':
            test_case.assertEqual(
                response.headers['Access-Control-Allow-Headers'],
                value
            )
        elif key == 'Methods' or key == 'Access-Control-Allow-Methods':
            test_case.assertEqual(
                response.headers['Access-Control-Allow-Methods'],
                value
            )
        elif key == 'Origin' or key == 'Access-Control-Allow-Origin':
            test_case.assertEqual(
                response.headers['Access-Control-Allow-Origin'],
                value
            )

# Verify that the given key exists in the response and has the given value
def key_val(test_case, response, key, val):
    print '\t\tBody contains "%s" and "%s" is correct' % (key, key)
    try:
        test_case.assertEqual(response.json()[key], val)
    except KeyError as error:
        self.fail('"%s" does not exist in response' % key)

# Verify that the given key exists in the response and starts with the given value
def key_val_start(test_case, response, key, val):
    print '\t\tBody contains "%s" and "%s" is correct' % (key, key)
    try:
        test_case.assertEqual(response.json()[key][0:len(val)], val)
    except KeyError as error:
        self.fail('"%s" does not exist in response' % key)

# Verify that the response has the given body
def body(test_case, response, val):
    print '\t\tResponse body is correct'
    test_case.assertEqual(response.text, val)
