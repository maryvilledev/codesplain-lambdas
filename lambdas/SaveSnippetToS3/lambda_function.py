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
def update_index_file(snippetKey, bucket, snippetData, user):
    try:
        indexData = s3.get_object(Bucket=bucket, Key=user + '/index.json')['Body'].read()
    except ClientError as error:
        indexData = '{}'

    index = json.loads(indexData)
    index[snippetKey] = snippetData
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
    accessToken = event['headers']['Authorization']
    userID = event['pathParameters']['user_id']

    #Invoke the auth. lambda to verify the accessToken mathches the userID for the requested resource
    lambda_auth = client.invoke(
        FunctionName=os.environ['authorizeTokenName'],
        Payload=json.dumps({'accessToken': accessToken, 'userID': userID}))

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
    snippetTitle = body['snippetTitle']
    snippetKey = urllib.quote(string.lower(re.sub(r'\s+', '_', snippetTitle)))
    key = userID + '/' + snippetKey

    bucket = os.environ['BucketName']
    if(bucket == None):
        print 'Must specify "BucketName" env var!'
        raise error

    save_to_s3(bucket, key, event['body'])

    update_index_file(
        snippetKey,
        bucket,
        {'snippetTitle': snippetTitle, 'language': 'python3', 'lastEdited': datetime.now().isoformat()},
        userID)
    return {
        'statusCode': '200',
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'key': snippetKey})
    }
