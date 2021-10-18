from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import boto3, botocore
import logging
import os
import json

print('Loading function')

R53_HOSTED_ZONE_ID = os.environ['r53HostedZoneId']
BL_ALB_DNS = os.environ['blueAlbDns']
GR_ALB_DNS = os.environ['greenAlbDns']
ALB_HOSTED_ZONE_ID = os.environ['albHostedZoneId']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('route53')

# Get slack token from SSM Parameter Store
#ssm = boto3.client('ssm')
#SLACK_TOKEN = ssm.get_parameter(Name='SLACK_TOKEN', WithDecryption=True)['Parameter']['Value']
#slack_client = WebClient(token=SLACK_TOKEN)
#SLACK_CHANNEL = os.environ['slackChannel']






def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    #print("value1 = " + event['key1'])
    #print("value2 = " + event['key2'])
    #print("value3 = " + event['key3'])
    #return event['key1']  # Echo back the first key value
    #raise Exception('Something went wrong')
    
    try:
        response = client.change_resource_record_sets(
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'AliasTarget': {
                            'DNSName': BL_ALB_DNS,
                            'EvaluateTargetHealth': True,
                            #'HostedZoneId': 'ZWKZPGTI48KDX', # hosted zone id for alb, not the route 53 itself
                            'HostedZoneId': ALB_HOSTED_ZONE_ID
                        },
                        'Name': 'service.mydomain.int',
                        'SetIdentifier': 'myAlb-blue',  # Optional value, if SetIdentifier is not unique, same dns record can be crated
                        'Type': 'A',
                        'Weight': int(event['blWeight']),
                    },
                },
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'AliasTarget': {
                            'DNSName': GR_ALB_DNS,
                            'EvaluateTargetHealth': True,
                            #'HostedZoneId': 'ZWKZPGTI48KDX', # hosted zone id for alb, not the route 53 itself
                            'HostedZoneId': ALB_HOSTED_ZONE_ID
                        },
                        'Name': 'service.mydomain.int',
                        'SetIdentifier': 'myAlb-green',   
                        'Type': 'A',
                        'Weight': int(event['grWeight']),
                    },
                },
            ],
            'Comment': 'ELB load balancers for the api endpoint',
        },
        # Depends on the type of resource that you want to route traffic to
        HostedZoneId=R53_HOSTED_ZONE_ID
        )
        request_id = response['ChangeInfo']['Id']
#        message = "request_id: " + request_id
#        send_message = slack_client.chat_postMessage(
#            channel = SLACK_CHANNEL,
#            text = message
#        )
#        assert send_message["message"]["text"] != ''
        return logger.info("request id: {}".format(request_id))
    except botocore.exceptions.ClientError as e:
        return logger.error("Boto3 ClientError: {}".format(e))
    

