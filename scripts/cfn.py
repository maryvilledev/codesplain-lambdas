import boto3
from boto3.s3.transfer import ClientError
import os
import json
import sys

def main(arg1):
    dateFormat = "[%H:%M %m.%d.%y]"
    rollback = False


    client = boto3.client('cloudformation')
    response = client.describe_stack_events(
        StackName=arg1
    )
    for event in response['StackEvents']:
        if event['ResourceType'] == 'AWS::CloudFormation::Stack' and event['ResourceStatus']  ==  'REVIEW_IN_PROGRESS':
            if rollback:
                print 'Deleting Stack'
                client.delete_stack(
                    StackName=arg1
                )
            return
        if event ['ResourceStatus'] == 'ROLLBACK_COMPLETE':
            rollback = True
        if event ['ResourceStatus'] == 'CREATE_FAILED' or ['ResourceStatus']  == 'UPDATE_FAILED':
            print 'Stack Event failed ' + event['Timestamp'].strftime(dateFormat)
            print event['ResourceType'] + ': ' + event['ResourceStatusReason']
        if event['ResourceType'] == 'AWS::CloudFormation::Stack':
            if event['ResourceStatus']  == 'UPDATE_COMPLETE':
                print event['LogicalResourceId'] + " updated " + event['Timestamp'].strftime(dateFormat)
                return

            elif event['ResourceStatus'] == 'CREATE_COMPLETE':
                print event['LogicalResourceId'] + " created" + event['Timestamp'].strftime(dateFormat)
                return



if __name__=='__main__':
    main(sys.argv[1])


# {u'StackId': 'arn:aws:cloudformation:us-west-2:296636357169:stack/CodesplainDev/c1b753a0-2110-11e7-9f8f-503ac9316835', u'EventId': '18a28ce0-3b09-11e7-9c59-50a68d01a629', u'ResourceStatus': 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS', u'ResourceType': 'AWS::CloudFormation::Stack', u'Timestamp': datetime.datetime(2017, 5, 17, 13, 59, 51, 169000, tzinfo=tzutc()), u'StackName': 'CodesplainDev', u'PhysicalResourceId': 'arn:aws:cloudformation:us-west-2:296636357169:stack/CodesplainDev/c1b753a0-2110-11e7-9f8f-503ac9316835', u'LogicalResourceId': 'CodesplainDev'}
