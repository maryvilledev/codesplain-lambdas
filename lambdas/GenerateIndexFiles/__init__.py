import os
import json

import boto3
from boto3 import ClientError

s3 = boto3.resource('s3')
bucket = s3.Bucket(os.environ['BUCKET_NAME'])

def get_dirs ():
    """Creates a dict of dir names to snippet names from the bucket"""
    dirs = {}
    for obj in bucket.objects.all():
        dirname = os.path.dirname(obj.key)
        basename = os.path.basename(obj.key)
        if not dirname in dirs:
            dirs[dirname] = [basename]
        else:
            dirs[dirname].append(basename)
    return dirs

def has_index (files):
    """Takes the contents of a folder and returns if there is an index file"""
    return 'index.json' in files

def create_index (dirname, files):
    """Takes a list of filenames and creates a dict that is an index of the files"""
    index = {}
    for filename in files:
        snippet_key = "%s/%s" % (dirname, filename)
        snippet_info = get_snippet_info(snippet_key)
        index[snippet_key] = snippet_info
    return index

def get_snippet_info(snippet_key):
    """Connects to s3 and gets info about the snippet"""
    obj = s3.Object(os.environ['BUCKET_NAME'], snippet_key)
    content = json.loads(obj.get())
    return {
        'snippetTitle': content['snippetTitle'],
        'language': content['snippetLanguage'],
        'lastEdited': obj.last_modified
    }

def lambda_handler(event, context):
    """Called by AWS"""
    ## Get all the directories
    dirs = get_dirs()
    for dirname in dirs:
        files = dirs[dirname]
        ## If the directory does not contain an index
        if not has_index(files):
            index = create_index(dirname, files)
            data = json.dumps(index)
            try:
                s3.put_object(Bucket=bucket, Key="%s/index.json" % dirname, Body=data)
            except ClientError as error:
                print "Error adding index to directory %s" % dirname