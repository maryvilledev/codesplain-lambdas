import boto3
from boto3.s3.transfer import ClientError
import os
import json
import sys

def main(arg1):
    dateFormat = "[%H:%M %m.%d.%y]"
    rollback = False


    client = boto3.client('cloudformation', region_name='us-west-2')
    response = client.describe_stack_events(
        StackName=arg1
    )
    for event in response['StackEvents']:
        # The beginning of the current Stack Event
        if event['ResourceType'] == 'AWS::CloudFormation::Stack':
            if event['ResourceStatus']  ==  'REVIEW_IN_PROGRESS' or event['ResourceStatus']  ==  'UPDATE_IN_PROGRESS':
                print 'Stack Deploy Failed'
                if rollback:
                    print 'Deleting Stack'
                    client.delete_stack(
                        StackName=arg1
                )
                return
        # Delet Stacks that were Rolled Back
        if event['ResourceStatus'] == 'ROLLBACK_COMPLETE':
            rollback = True
        # Catch and log stack failures
        if event['ResourceStatus'] == 'CREATE_FAILED' or event['ResourceStatus']  == 'UPDATE_FAILED':
            print 'Stack Event failed ' + event['Timestamp'].strftime(dateFormat)
            print event['ResourceType'] + ': ' + event['ResourceStatusReason']
        # If Cloudformation Stack Complete or Update Complete, log and return
        if event['ResourceType'] == 'AWS::CloudFormation::Stack':
            if event['ResourceStatus']  == 'UPDATE_COMPLETE':
                print event['LogicalResourceId'] + " updated " + event['Timestamp'].strftime(dateFormat)
                return

            elif event['ResourceStatus'] == 'CREATE_COMPLETE':
                print event['LogicalResourceId'] + " created" + event['Timestamp'].strftime(dateFormat)
                return



if __name__=='__main__':
    main(sys.argv[1])
