import os
import requests
from requests.exceptions import HTTPError

import boto3

s3 = boto3.resource('s3')


def lambda_handler(event, context):

    bucket_name = os.environ['BucketName']
    bucket = s3.Bucket(bucket_name)
    for object in bucket.objects.all():
        print(object)
        object.delete()

    circle_URL = "https://circleci.com/api/v1.1/project/github/maryvilledev/codesplainUI/tree/master?circle-token=" + os.environ['CircleCIToken']
    r = requests.post(circle_URL)
    print(r.status_code)
