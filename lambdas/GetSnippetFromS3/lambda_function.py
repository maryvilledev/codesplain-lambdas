import boto3
from boto3.s3.transfer import ClientError
import os
import json

s3 = boto3.client('s3', 'us-west-2')
client = boto3.client('lambda')

def get_from_s3(bucket, key):
    try:
        s3.get_object(Bucket=bucket, Key=key)
    except ClientError as error:
        err_code = str(error.response['Error']['Code'])
        print 'Error getting object %s from bucket %s' % (key, bucket)
        return {
                'statusCode': '400',
                'headers': {'Access-Control-Allow-Origin': '*'}
                }

def lambda_handler(event, context):
    key = event['pathParameters']['user_id'] + '/' + event['pathParameters']['snippet_id']
    bucket = os.environ['BucketName']

    get_from_s3(bucket, key, event['body'])
    return {
        'statusCode': '200',
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({event['body']})
    }
