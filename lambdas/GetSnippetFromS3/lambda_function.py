import boto3
from boto3.s3.transfer import ClientError
import os
import json

s3 = boto3.client('s3', 'us-west-2')
client = boto3.client('lambda')

def lambda_handler(event, context):
    key = event['pathParameters']['user_id'] + '/' + event['pathParameters']['snippet_id']
    bucket = os.environ['BucketName']

    if(bucket == None):
        print 'Must specify "BucketName" env var!'
        raise error
    try:
        object = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
        print object
    except ClientError as error:
        print 'Error getting object %s from bucket %s' % (key, bucket)
        return {
                'statusCode': '404',
                'body': 'No snippet exists with key "%s"' % key,
                'headers': {'Access-Control-Allow-Origin': '*'}
        }
    return {
        'statusCode': '200',
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': object
    }
