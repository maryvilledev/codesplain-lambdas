#!/bin/env python

import boto3
from boto3.s3.transfer import ClientError
import os
import json

def main():
    print 'Parsing CFN for '



    client = boto3.client('cloudformation')
    response = client.describe_stack_events(
        StackName='CodesplainFeature-jefe'
    )
    for event in response['StackEvents']:
        if event['ResourceType'] == 'AWS::CloudFormation::Stack':
            if event['ResourceStatus']  == 'UPDATE_COMPLETE' or event['ResourceStatus'] == 'CREATE_COMPLETE':
                print event['LogicalResourceId'] + " Updated"
                return


if __name__=='__main__':
    main()
