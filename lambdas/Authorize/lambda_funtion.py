import os
import json
import requests
from boto3.s3.transfer import ClientError

s3 = boto3.client('s3', 'us-west-2')
client = boto3.client('lambda')

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

def generate_policy(prinicipal_id, effect, resource):
    return {
        prinicipal_id,
        policy_document: {
        Version: '2012-10-17'
        Statements: [{
            Action: 'execute-api:Invoke',
            Effect: effect,
            Resource: resource
        }]
    }
}

def lambda_handler(event, context):    
    token = event['authorizationToken']

    requests.get('https://api.github.com/applications/ %s/tokens/ %s' % (client_id, token), auth=('client_id', 'token'))

    try:
        generate_policy('user', 'Allow', event[methodArn])
    except ClientError as error:
        print 'Unauthorized'
