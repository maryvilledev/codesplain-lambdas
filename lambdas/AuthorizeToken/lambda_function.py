import os
import requests

user_url = 'https://api.github.com/user'
org_url = 'https://api.github.com/user/orgs'

def generate_resp(code, body):
    return {
    'statusCode': code,
    'headers': {'Access-Control-Allow-Origin': '*'},
    'body': body
    }

def is_valid(role, user, orgs):
    """Combine user and orgs into valid roles and test for membership"""
    roles = orgs + [user]
    return role in set(roles)

def lambda_handler(event, context):
    role = event['userID']
    access_token = event['accessToken']
    headers = {'Accept': 'application/json', 'Authorization': access_token}

    try:
        r = requests.get(user_url, headers=headers)
        r.raise_for_status()
        user = r.json()['login']
        r = requests.get(org_url, headers=headers)
        r.raise_for_status()
        orgs = map(lambda x: x['login'], r.json())
        #1.1 If GitHub communication error throw 500 code
    except requests.exceptions.HTTPError as error:
        return generate_resp(500, error)

    if is_valid(role, user, orgs):
        return generate_resp(200, 'Authorized')

    return generate_resp(400, 'Not Authorized to acces this resource')
