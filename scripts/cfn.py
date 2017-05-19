import boto3
from boto3.s3.transfer import ClientError
import os
import json
import sys

DATE_FORMAT = "[%H:%M %m.%d.%y]"

def printTime(timestamp):
    return timestamp.strftime(DATE_FORMAT)


def main(stack_name):
    rollback = False


    client = boto3.client('cloudformation', region_name='us-west-2')
    response = client.describe_stack_events(
        StackName=stack_name
    )
    for event in response['StackEvents']:
        # The beginning of the current Stack Event
        if event['ResourceType'] == 'AWS::CloudFormation::Stack':
            if event['ResourceStatus']  ==  'REVIEW_IN_PROGRESS' or event['ResourceStatus']  ==  'UPDATE_IN_PROGRESS':
                print 'Stack Deploy Failed'
                if rollback:
                    print 'Deleting Stack'
                    client.delete_stack(
                        StackName=stack_name
                        )
                return
        # Delet Stacks that were Rolled Back
        if event['ResourceStatus'] == 'ROLLBACK_COMPLETE':
            rollback = True
        # Catch and log stack failures
        if event['ResourceStatus'] == 'CREATE_FAILED' or event['ResourceStatus']  == 'UPDATE_FAILED':
            print 'Stack Event failed ' + printTime(vent['Timestamp'])
            print event['ResourceType'] + ': ' + event['ResourceStatusReason']
        # If Cloudformation Stack Complete or Update Complete, log and return
        if event['ResourceType'] == 'AWS::CloudFormation::Stack':
            if event['ResourceStatus']  == 'UPDATE_COMPLETE':
                print event['LogicalResourceId'] + " updated " + printTime(event['Timestamp'])
                return

            elif event['ResourceStatus'] == 'CREATE_COMPLETE':
                print event['LogicalResourceId'] + " created" + printTime(event['Timestamp'])
                return



if __name__=='__main__':
    main(sys.argv[1])
