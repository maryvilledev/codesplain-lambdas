import os
import requests
from requests.exceptions import HTTPError

import boto3

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    # bucket_name = os.environ['BucketName']
    # bucket = s3.Bucket(bucket_name)
    # for object in bucket.objects.all():
    #     print(object)
    #     object.delete()


    try:
        requests.post("https://www.circleci.com/api/v1.1/project/github/maryvilledev/codesplainUI/tree/master?circle-token=a8535f85bf092db8d4fbdcfe6aef56a1cf8c587f")
    except HTTPError:
        print(HTTPError)
