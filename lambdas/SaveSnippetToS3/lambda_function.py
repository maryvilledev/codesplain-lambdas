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

#Verifies existance of index file; if absent, creates index file. Writes file to S3.
def update_index_file(snippet_key, bucket, snippet_data, user):
    try:
        index_data = s3.get_object(Bucket=bucket, Key=user + '/index.json')['Body'].read()
    except ClientError as error:
        index_data = '{}'

    index = json.loads(index_data)
    index[snippet_key] = snippet_data
    s3.put_object(Body=json.dumps(index), Bucket=bucket, Key=user +'/index.json')

#Saves the given body to the appropiate bucket under the assigned key.
def save_to_s3(bucket, key, body):
    try:
        s3.put_object(Body=body, Bucket=bucket, Key=key)
    except ClientError as error:
        err_code = str(error.response['Error']['Code'])
        print 'Error putting object %s into bucket %s. Make sure they exist and ' \
              'your bucket is in the same region as this function.' % (key, bucket)
        raise error

def lambda_handler(event, context):
    #Extract needed data from the event
    access_token = event['headers']['Authorization']
    user_id = event['pathParameters']['user_id']

    #Invoke the auth. lambda to verify the accessToken mathches the user_id for the requested resource
    lambda_auth = client.invoke(
        FunctionName=os.environ['authorizeTokenName'],
        Payload=json.dumps({'accessToken': access_token, 'userID': user_id}))

    lambda_payload_resp = json.loads(lambda_auth['Payload'].read())

    if(lambda_payload_resp['statusCode'] == '400'):
        return {'statusCode': '400', 'body': json.dumps({'response': lambda_payload_resp['body']})}

    # -------- Otherwise, save to S3 -------- #
    if(event['body'] == None):
        return {
            'statusCode': '400',
            'headers':    { 'Access-Control-Allow-Origin': '*' },
            'body':       json.dumps({
               'response': 'POST requests must not have empty bodies.'
            })
        }
    body = json.loads(event['body'])
    snippet_title = body['snippetTitle']
    snippet_key = urllib.quote(string.lower(re.sub(r'\s+', '_', snippet_title)))
    key = user_id + '/' + snippet_key

    bucket = os.environ['BucketName']
    if(bucket == None):
        print 'Must specify "BucketName" env var!'
        raise error

    save_to_s3(bucket, key, event['body'])

    update_index_file(
        snippet_key,
        bucket,
        {'snippetTitle': snippet_title, 'language': body['snippetLanguage'], 'lastEdited': datetime.now().isoformat()},
        user_id)
    return {
        'statusCode': '200',
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'key': snippet_key})
    }
