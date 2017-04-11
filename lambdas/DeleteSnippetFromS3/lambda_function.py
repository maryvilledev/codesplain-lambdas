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

def deleteObjFromS3(bucket, key):
    try:
        s3.delete_object(Bucket=bucket, Key=key)
    except ClientError as error:
        err_code = str(error.response['Error']['Code'])
        print 'Error deleting object %s from bucket %s. Make sure ' \
              'your bucket is in the same region as this function.' % (key, bucket)
        raise error

def object_exists(bucket, key):
    try:
        contentsInBucket = s3.head_object(Bucket=bucket, Key=key)
    except ClientError as error:
        return False
    return True

#Verifies existance of index file; if absent, creates index file. Writes file to S3.
def updateIndexFile(snippetKey, bucket, user):
    try:
        indexData = s3.get_object(Bucket=bucket, Key=user + '/index.json')['Body'].read()
    except ClientError as error:
        indexData = '{}'

    index = json.loads(indexData)
    del index[snippetKey]
    s3.put_object(Body=json.dumps(index), Bucket=bucket, Key=user +'/index.json')

def lambda_handler(event, context):
    #Extract needed data from the event
    accessToken = event['headers']['Authorization']
    userID = event['pathParameters']['user_id']

    authorizeTokenName = os.environ['authorizeTokenName']

    #Invoke the auth. lambda to verify the accessToken mathches the userID for the requested resource
    lambda_auth = client.invoke(
        FunctionName = os.environ['authorizeTokenName'],
        Payload=json.dumps({'accessToken': accessToken, 'userID': userID}))

    lambda_payload_resp = json.loads(lambda_auth['Payload'].read())

    if(lambda_payload_resp['statusCode'] == '400'):
        return {'statusCode': '400', 'body': json.dumps({'response': lambda_payload_resp['body']})}

    # -------- Otherwise, delete from S3 -------- #
    snippetKey = event['pathParameters']['snippet_id']
    key = userID + '/' + snippetKey
    apiID = event['requestContext']['apiId']
    bucket = os.environ['BucketName']

    if (not object_exists(bucket, key)):
        return {'statusCode': '400', 'body':json.dumps({'response': snippetKey + ' does not exist'})}
    else:
        deleteObjFromS3(bucket, key)

    updateIndexFile(
        snippetKey,
        bucket,
        userID)
    return {
        'statusCode': '200',
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'response': 'Successfully deleted.'})
    }
