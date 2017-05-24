import json
import urllib
import re
import os
from datetime import datetime
from boto3.s3.transfer import ClientError
import string
import boto3 # AWS SDK for Python

s3 = boto3.client('s3', 'us-west-2')
client = boto3.client('lambda')
s3_resource = boto3.resource('s3')

# Returns time the s3 Object was last modified
def get_last_modified(s3Object):
    return s3Object.last_modified.isoformat()

# Returns the snippet key with the lowest possible unused postfix value.
def generate_snippet_id(bucket, user_id, snippet_title):
    snippet_id = urllib.quote_plus(string.lower(re.sub(r'\s+', '_', snippet_title)))
    if object_exists(bucket, user_id, snippet_id):
        return generate_snippet_id(bucket, user_id, next_title(snippet_title))
    return snippet_id

# Increments the postfix on the given snippet_title and returns the result.
# If the given snippet_title has not postfix, '-1' will be appended.
def next_title(snippet_title):
    postfix_idx = snippet_title.rfind('-')
    if postfix_idx == -1 or (postfix_idx + 1) > len(snippet_title):
        return snippet_title + '-1'
    postfix    = snippet_title[postfix_idx + 1 : len(snippet_title)]
    new_postfix = int(postfix) + 1
    return snippet_title[0 : postfix_idx + 1] + str(new_postfix)

# Returns true if given snippet_id exists under given user in the given bucket.
# Returns false if not.
def object_exists(bucket, user_id, snippet_id):
    try:
        s3.head_object(
            Bucket=bucket,
            Key=user_id + '/' + snippet_id
        )
    except ClientError as error:
        return False
    return True

# Updates index file and writes to S3. Creates new one if needed.
def update_index_file(bucket, user_id, snippet_key, entry):
    key = user_id + '/index.json'
    try:
        index_str = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
    except ClientError as error:
        index_str = '{}'

    index = json.loads(index_str)
    index[snippet_key] = entry
    s3.put_object(Body=json.dumps(index), Bucket=bucket, Key=key)

# Saves the given body to the given bucket under the given key
def save_to_s3(bucket, user_id, snippet_key, body):
    s3Bucket = s3.Bucket(bucket)
    key = user_id + '/' + snippet_key
    try:
        s3Obj = s3Bucket.put_object(Body=body, Bucket=bucket, Key=key)
    except ClientError as error:
        print 'Error putting object %s into bucket %s. Make sure your bucket ' \
        'exists and is in the same region as this function.' % (key, bucket)
        raise error
    return s3Obj

# Lambda handler function
def lambda_handler(event, context):
    # Extract needed data from the event
    access_token = event['headers']['Authorization']
    user_id      = event['pathParameters']['user_id']

    # Invoke the authorization lambda to verify the
    # accessToken matches the user_id for the requested resource
    lambda_auth = client.invoke(
        FunctionName=os.environ['authorizeTokenName'],
        Payload=json.dumps({
            'accessToken': access_token,
            'userID': user_id
        }))

    # Respond with 401 is user is not authorized
    resp_payload = json.loads(lambda_auth['Payload'].read())
    if(resp_payload['statusCode'] == '400'):
        return {
            'statusCode': '401',
            'body': json.dumps({
                'response': lambda_payload_resp['body']
            })
        }

    # -------- Otherwise, user is authorized, so save to S3 -------- #
    body             = json.loads(event['body'])
    snippet_title    = body['snippetTitle']
    snippet_language = body['snippetLanguage']
    bucket           = os.environ['BucketName']
    if(bucket == None):
        print 'Must specify "BucketName" env var!'
        raise error
    snippet_id = generate_snippet_id(bucket, user_id, snippet_title)

    s3Obj = save_to_s3(bucket, user_id, snippet_id, event['body'])
    new_entry = {
        'snippetTitle': snippet_title,
        'language':     snippet_language,
        'lastEdited':   get_last_modified(s3Obj),
    }
    update_index_file(bucket, user_id, snippet_id, new_entry)
    return {
        'statusCode': '200',
        'headers':    { 'Access-Control-Allow-Origin': '*' },
        'body':       json.dumps({ 'key': snippet_id })
    }
