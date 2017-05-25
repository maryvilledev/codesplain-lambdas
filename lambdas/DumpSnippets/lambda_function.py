import os
import json
import boto3
import zipfile
import base64

# Initialization
s3 = boto3.client('s3', 'us-west-2')
try:
    bn = os.environ['BucketName']
except KeyError as error:
    print 'Must specify "BucketName" env var!'
    raise error
try:
    zb = os.environ['ZipsBucket']
except KeyError:
    zb = 'codesplain-zips'
snippets_bucket = boto3.resource('s3').Bucket(bn)
zips_bucket     = boto3.resource('s3').Bucket(zb)


def zip_snippets(snippet_keys):
    """Writes the contents of the snippets with given keys to a zip file,
       returns the path to the zip."""
    zip_path = '/tmp/dump.zip'
    with zipfile.ZipFile(zip_path, 'w') as dump_zip:
        for key in snippet_keys:
            snippet  = snippet_contents(key)
            filename = os.path.basename(key)
            dump_zip.writestr(filename, snippet)
    return zip_path

def move_to_zips_bucket(source, dest):
    """Copies the source file to the zips_bucket under dest path, returns
       publicly-accessible URL for that new resource."""
    zips_bucket.upload_file(source, dest)
    return s3.generate_presigned_url('get_object', Params = {
        'Bucket': zips_bucket.name,
        'Key': dest,
    })

def snippet_contents(key):
    """Returns contents of specified snippet as string"""
    return s3.get_object(Bucket=snippets_bucket.name, Key=key)['Body'].read()

def user_snippet_keys(user):
    """Returns the object keys ("absolute paths") to each of
       a user's snippets, including their index.json file"""
    keys = []
    for obj in snippets_bucket.objects.all():
        if user == owner(obj.key):
            keys.append(obj.key)
    return keys

def owner(snippet_path):
    """Returns the owner of the snippet with specified path"""
    dirname = os.path.dirname(snippet_path)
    owner = dirname[dirname.rfind('/') + 1 :]
    return owner

def lambda_handler(event, context):
    """Called by AWS"""
    user     = event['pathParameters']['user_id']
    dest     = user + '/snippets.zip'
    keys     = user_snippet_keys(user)
    zip_path = zip_snippets(keys)
    url      = move_to_zips_bucket(zip_path, dest)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/zip',
    }
    return {
        'statusCode': 200,
        'headers':    headers,
        'body':       url,
    }
