import json
import urllib
import os
from datetime import datetime
from boto3.s3.transfer import ClientError
import boto3 # AWS SDK for Python

s3     = boto3.client('s3', 'us-west-2')
client = boto3.client('lambda')

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
    key = user_id + '/' + snippet_key
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=body)
    except ClientError as error:
        print 'Error putting object %s into bucket %s. Make sure your bucket ' \
        'exists and is in the same region as this function.' % (key, bucket)
        raise error

# Lambda handler function
def lambda_handler(event, context):
    # Extract stuff we need from the event
    access_token = event['headers']['Authorization']
    user_id      = event['pathParameters']['user_id']
    snippet_id   = event['pathParameters']['snippet_id']

    # Invoke the authorization lambda to ensure the access_token
    # included in the request matches the user_id for the requested
    # resource.
    resp = client.invoke(
        FunctionName=os.environ['authorizeTokenName'],
        Payload=json.dumps({
            'accessToken': access_token,
            'userID': user_id
        }))

    # Respond with 401 if user is not authorized
    resp_payload = json.loads(resp['Payload'].read())
    if(resp_payload['statusCode'] == '400'):
        return {
            'statusCode': '401',
            'body': json.dumps({
                'response': resp_payload['body']
            })
        }

    # ----- Otherwise, user is authorized, so save to S3 ----- #
    body   = json.loads(event['body'])
    bucket = os.environ['BucketName']
    if(bucket == None):
        print 'Must specify "BucketName" env var!'
        raise error

    save_to_s3(bucket, user_id, snippet_id, event['body'])
    new_entry = {
        'snippetTitle': body['snippetTitle'],
        'language':     body['snippetLanguage'],
        'lastEdited':   datetime.utcnow().isoformat()
    }
    update_index_file(bucket, user_id, snippet_id, new_entry)
    return {
        'statusCode': '200',
        'headers':    { 'Access-Control-Allow-Origin': '*' },
        'body':       json.dumps({ 'key': snippet_id })
    }
