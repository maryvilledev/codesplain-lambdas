import os
import json
from boto3.s3.transfer import ClientError
import requests

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

def generate_policy(prinicipal_id, effect, resource):
    return {
        'prinicipal_id': prinicipal_id,
        'policy_document': {
            'Version': '2012-10-17',
            'Statements': [{
            'Action': 'execute-api:Invoke',
            'Effect': effect,
            'Resource': resource
        }]
    }
}

def lambda_handler(event, context):
    token = event['authorizationToken']
    url = 'https://api.github.com/applications/{client_id}/tokens/{token}'.format(client_id, token)
    try:
        requests.get(url, auth=(client_id, client_secret)).raise_for_status()
    except ClientError as error:
        return {'body': 'Unauthorized'}
    return generate_policy('user', 'Allow', event['methodArn'])
