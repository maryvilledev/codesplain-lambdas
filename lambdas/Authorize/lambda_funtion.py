import os
import json
import requests
from boto3.s3.transfer import ClientError

s3 = boto3.client('s3', 'us-west-2')
client = boto3.client('lambda')

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

def auth_request(client_id, client_secret):
    requests.get('https://api.github.com/applications/ %s/tokens/ %s' % (client_id, token), auth=('client_id', 'client_secret'))

def generate_policy(principalId, effect, resource):
    return {
        'principalId',
        'policyDocument': {
          'Version': '2012-10-17',
          'Statement': [{
            'Action': 'execute-api:Invoke',
            'Effect': effect,
            'Resource': resource
          }]
        }
    }

def lambda_handler(event, context):
    token = event['authorizationToken']
    try:
        auth_request(token)
    except ClientError as error:
        print 'Unauthorized'

    generate_policy(user, Allow, event[methodArn])
