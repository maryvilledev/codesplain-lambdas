import os
import json
import boto3
from boto3.s3.transfer import ClientError

s3 = boto3.client('s3', 'us-west-2')

def snippet_contents(bucket, key):
    """Returns contentnts of specified snippet as string"""
    return s3.get_object(Bucket=bucket, Key=key)['Body'].read()

def user_snippet_keys(s3_bucket, user):
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

    # Initialization
    user = event['pathParameters']['user_id']
    bucket = os.environ['BucketName']
    if bucket == None:
        print 'Must specify "BucketName" env var!'
        raise error
    s3_bucket = boto3.resource('s3').Bucket(bucket)

    # Generate the dump JSON
    dump = {}
    for key in user_snippet_keys(s3_bucket, user):
        print 'adding to dump: ' + key
        dump[key] = snippet_contents(bucket, key)
    print 'completed dump: '
    print dump

    # Send response
    return {
        'statusCode': 200,
        'headers':    { 'Access-Control-Allow-Origin': '*' },
        'body':       json.dumps(dump),
    }
