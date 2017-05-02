import boto3
from boto3.s3.transfer import ClientError
import os
import json

print 'running GetIndexes lambda'

s3 = boto3.client('s3', 'us-west-2')
client = boto3.client('lambda')

# Gets the environment variable with the given name. If it
# is not defined, then an error is raised.
def get_env_var(name):
    var = os.environ['BucketName']
    if var == None:
        print 'Must specify "%s" env var!' % name
        raise error
    return var

# Returns all users in the given bucket, where a user is the
# substring of an object's key from index 0 to the first '/' char.
def get_all_users(bucket):
    objects = s3.list_objects(Bucket=bucket)['Contents']
    users = set()
    for obj in objects:
        users.add(obj['Key'].split('/')[0])
    return users

# Parses the given event object for the "users" query param.
# Returns its value parsed as a list. If the param does not
# exist, returns all users in the given bucket.
def get_users(bucket, event):
    query_params = event['queryStringParameters']
    if query_params != None and 'users' in query_params:
        users = query_params['users'].split(',')
    else:
        users = get_all_users(bucket)
    return users

# Returns true if the given user exists in the given bucket,
# false if not
def user_exists(bucket, user):
    key = user + '/index.json'
    try:
        s3.head_object(Bucket=bucket, Key=key)
    except ClientError as error:
        return False
    return True

# Gets the index file for the given user within the given
# bucket, parses it, and adds it to the given dict. If the
# user has no index file (does not exist), an empty object
# will be used.
def add_user_index(dict, bucket, user):
    if user_exists(bucket, user):
        key = user + '/index.json'
        index = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
        dict[user] = json.loads(index)
    else:
        dict[user] = '{}'

# Returns a JSON object where each entry's key is a user, and its value
# is that user's index.json. The "users" query param is used to filter
# on users, e.g. "?users=foo,bar,qux,baz". If the "users" param is not
# present, the returned JSON will contain all the users.
def lambda_handler(event, context):
    bucket = get_env_var('BucketName')
    users  = get_users(bucket, event)

    return_dict = {}
    for user in users:
        add_user_index(return_dict, bucket, user)

    return {
        'statusCode': '200',
        'headers': { 'Access-Control-Allow-Origin': '*' },
        'body': json.dumps(return_dict),
    }
