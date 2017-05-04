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
        print 'Bucket=%s' % bucket
        print 'Key=%s' % key
        object = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
    except ClientError as error:
        print 'Error getting object %s from bucket %s' % (key, bucket)
        print error
        return {
                'statusCode': '400',
                'headers': {'Access-Control-Allow-Origin': '*'}
        }
    return {
        'statusCode': '200',
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': object
    }
