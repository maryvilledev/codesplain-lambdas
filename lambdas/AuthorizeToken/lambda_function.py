import os
import json
import requests
import boto3
from boto3.s3.transfer import ClientError

s3 = boto3.client('s3', 'us-west-2')
client = boto3.client('lambda')

def authorize_token(acces_token, username):
    headers = {'Accept': 'application/json', 'Authorization': token['acces_token']}
    url = 'https://api.github.com/user'
    try:
        requests.get(url, headers=headers)
        return {'statusCode': '200', 'body': 'Authorized to access this resource'}
    except ClientError as error:
        return {'statusCode': '400', 'body': 'Not authorized to access this resource'}
              #TODO:// Do better than this

def lambda_handler(event, context):
    try:
        authorize_token(event['acces_token'], event['user_id'])
    except Exception as error:
        return {'statusCode': '500', 'body': json.dumps({'response': 'response'})}
