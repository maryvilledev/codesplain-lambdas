import os
import requests
from requests.exceptions import HTTPError

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

def generate_policy(principal_id, effect, resource):
    return {
        'principalId': principal_id,
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
    url = 'https://api.github.com/applications/%s/tokens/%s' % (client_id, token)
    try:
        requests.get(url, auth=(client_id, client_secret)).raise_for_status()
    except HTTPError:
        return {"errorMessage": "Unauthorized"} 
    return generate_policy('user', 'Allow', event['methodArn'])
