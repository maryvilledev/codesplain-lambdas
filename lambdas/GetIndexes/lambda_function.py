import boto3
from boto3.s3.transfer import ClientError
import os
import json

s3 = boto3.client('s3', 'us-west-2')
client = boto3.client('lambda')

def lambda_handler(event, context):
    print 'running GetIndexes lambda'
    return {
        'statusCode': '200',
        'headers': {'Access-Control-Allow-Origin': '*'},
    }
