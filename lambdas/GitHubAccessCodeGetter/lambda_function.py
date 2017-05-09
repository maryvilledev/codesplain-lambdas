import os
import requests
import json

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
org_whitelist = os.environ['ORG_WHITELIST'].split(';')
ignore_whitelist = os.environ['IGNORE_WHITELIST']

def generate_resp(code, body):
    return {
    'statusCode': code,
    'headers': {'Access-Control-Allow-Origin': '*'},
    'body': body
    }

def lambda_handler(event, context):
    #Get the code from event body
    code = json.loads(event)['body']['code']

    #Get the token from GitHub
    url = 'https://github.com/login/oauth.access_token'
    data = {'client_id': client_id, 'client_secret': client_secret, 'code': code}
    r = requests.get(url, data=data)
    if r.status_code != 200:
        return generate_resp(400, 'The authorization code is invalid')

    #Get the user orgs
    if ignore_whitelist.lower() != 'true':
        url = 'https://api.github.com/user/orgs'
        headers = {'Authorization': 'token'}
        r = requests.get(url, headers=headers)
        user_orgs = map(lambda x: x['login'], r.json())
        if len(intersection(set(user_orgs), set(whitelist)) > 0:
            return generate_resp(403, 'You are not a member of an organization authorized to use this application.')

    #Return token and orgs to  user with code 200
    return generate_resp(200, json.dumps({'token': token, 'orgs': user_orgs}))
