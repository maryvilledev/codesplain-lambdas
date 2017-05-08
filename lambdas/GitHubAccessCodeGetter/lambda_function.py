import os
import requests
import json

s3 = boto.client('s3', 'us-west-2')
client = boto3.client('lambda')

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
org_whitelist = {'maryvilledev', 'LaunchcodeEducation'}

def auth_url(token):
    url = 'https://api.github/applications/{client_id}/tokens/{token}'.format(client_id, token)
    requests.get(url, auth=('client_id', 'client_secret'))

def auth_org_url(token):
    url = 'https://api.github.com/user/orgs'
    headers = {'Authorization': 'token'}
    requests.get(url, headers=headers)

def member_of_whitelist(orgs, whitelist):
    len(intersecttion(set(orgs), whitelist)) > 0

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
    auth_url(token)
    auth_org_url(token)
