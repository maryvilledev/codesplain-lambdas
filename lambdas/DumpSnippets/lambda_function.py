import os
import json
import boto3
import zipfile
import base64

# Initialization
s3 = boto3.client('s3', 'us-west-2')
bucket_name = os.environ['BucketName']
if bucket_name == None:
    print 'Must specify "BucketName" env var!'
    raise error
s3_bucket = boto3.resource('s3').Bucket(bucket_name)

def b64_zip_snippets(snippet_keys):
    """Writes the contents of the snippets with given keys to a zip file
       and returns the raw base64 encoded zip file"""
    zip_path = '/tmp/dump.zip'
    with zipfile.ZipFile(zip_path, 'w') as dump_zip:
        for key in snippet_keys:
            snippet  = snippet_contents(key)
            filename = os.path.basename(key)
            if (filename != 'index.json')
                filename = filename + '.json'
            dump_zip.writestr(filename, snippet)
    with open(zip_path, 'r') as dump_zip:
        return base64.b64encode(dump_zip.read())

def snippet_contents(key):
    """Returns contentnts of specified snippet as string"""
    return s3.get_object(Bucket=bucket_name, Key=key)['Body'].read()

def user_snippet_keys(user):
    """Returns the object keys ("absolute paths") to each of
       a user's snippets, including their index.json file"""
    keys = []
    for obj in s3_bucket.objects.all():
        if user == owner(obj.key):
            keys.append(obj.key)
    return keys

def owner(snippet_path):
    """Returns the owner of the snippet with specified path"""
    dirname = os.path.dirname(snippet_path)
    owner = dirname[dirname.rfind('/') + 1 :]
    return owner

def lambda_handler(event, context):
    """Called by AWS"""
    user    = event['pathParameters']['user_id']
    keys    = user_snippet_keys(user)
    b64_zip = b64_zip_snippets(keys)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/zip',
    }
    return {
        'statusCode': 200,
        'headers':    headers,
        'body':       b64_zip,
    }
