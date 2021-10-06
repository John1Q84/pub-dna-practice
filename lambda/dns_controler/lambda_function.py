from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import boto3, botocore
import logging
import os
import json

print('Loading function')

R53_HOSTED_ZONE = os.environ['hostedZone']
#BLUE_WEIGHT = int(os.environ['blWeight'])
#GREEN_WEIGHT = int(os.environ['grWeight'])



logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('route53')

# Get slack token from SSM Parameter Store
ssm = boto3.client('ssm')
SLACK_TOKEN = ssm.get_parameter(Name='SLACK_TOKEN', WithDecryption=True)['Parameter']['Value']
SLACK_CHANNEL = os.environ['slackChannel']
slack_client = WebClient(token=SLACK_TOKEN)

'''
# default example # 
response = client.change_resource_record_sets(
    HostedZoneId='string',
    ChangeBatch={
        'Comment': 'string',
        'Changes': [
            {
                'Action': 'CREATE'|'DELETE'|'UPSERT',
                'ResourceRecordSet': {
                    'Name': 'string',
                    'Type': 'SOA'|'A'|'TXT'|'NS'|'CNAME'|'MX'|'NAPTR'|'PTR'|'SRV'|'SPF'|'AAAA'|'CAA'|'DS',
                    'SetIdentifier': 'string',
                    'Weight': 123,
                    'Region': 'us-east-1'|'us-east-2'|'us-west-1'|'us-west-2'|'ca-central-1'|'eu-west-1'|'eu-west-2'|'eu-west-3'|'eu-central-1'|'ap-southeast-1'|'ap-southeast-2'|'ap-northeast-1'|'ap-northeast-2'|'ap-northeast-3'|'eu-north-1'|'sa-east-1'|'cn-north-1'|'cn-northwest-1'|'ap-east-1'|'me-south-1'|'ap-south-1'|'af-south-1'|'eu-south-1',
                    'GeoLocation': {
                        'ContinentCode': 'string',
                        'CountryCode': 'string',
                        'SubdivisionCode': 'string'
                    },
                    'Failover': 'PRIMARY'|'SECONDARY',
                    'MultiValueAnswer': True|False,
                    'TTL': 123,
                    'ResourceRecords': [
                        {
                            'Value': 'string'
                        },
                    ],
                    'AliasTarget': {
                        'HostedZoneId': 'string',
                        'DNSName': 'string',
                        'EvaluateTargetHealth': True|False
                    },
                    'HealthCheckId': 'string',
                    'TrafficPolicyInstanceId': 'string'
                }
            },
        ]
    }
)

###########################################
# sample request code #
The following example creates two weighted resource record sets. 
The resource with a Weight of 100 will get 1/3rd of traffic (100/100+200), 
and the other resource will get the rest of the traffic for example.com.


response = client.change_resource_record_sets(
    ChangeBatch={
        'Changes': [
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'AliasTarget': {
                        'DNSName': 'example-com-123456789.us-east-2.elb.amazonaws.com ',
                        'EvaluateTargetHealth': True,
                        'HostedZoneId': 'Z3AADJGX6KTTL2', # hosted zone id for alb, not the route 53 itself
                    },
                    'Name': 'example.com',
                    'SetIdentifier': 'Ohio region',  # can be omitted
                    'Type': 'A',
                    'Weight': 100,
                },
            },
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'AliasTarget': {
                        'DNSName': 'example-com-987654321.us-west-2.elb.amazonaws.com ',
                        'EvaluateTargetHealth': True,
                        'HostedZoneId': 'Z1H1FL5HABSF5',
                    },
                    'Name': 'example.com',
                    'SetIdentifier': 'Oregon region',   # can be omitted
                    'Type': 'A',
                    'Weight': 200,
                },
            },
        ],
        'Comment': 'ELB load balancers for example.com',
    },
    # Depends on the type of resource that you want to route traffic to
    HostedZoneId='Z3M3LMPEXAMPLE',
)

print(response)
'''



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
                            'DNSName': 'dualstack.myalb-blue-1937821487.ap-northeast-2.elb.amazonaws.com',
                            'EvaluateTargetHealth': True,
                            'HostedZoneId': 'ZWKZPGTI48KDX', # hosted zone id for alb, not the route 53 itself
                        },
                        'Name': 'api-endpoint.my-awsome-app.xyz',
                        'SetIdentifier': 'blue-endpoint',  # Optional value, if SetIdentifier is not unique, same dns record can be crated
                        'Type': 'A',
                        'Weight': int(event['blWeight']),
                    },
                },
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'AliasTarget': {
                            'DNSName': 'dualstack.myalb-green-260296419.ap-northeast-2.elb.amazonaws.com',
                            'EvaluateTargetHealth': True,
                            'HostedZoneId': 'ZWKZPGTI48KDX', # hosted zone id for alb, not the route 53 itself
                        },
                        'Name': 'api-endpoint.my-awsome-app.xyz',
                        'SetIdentifier': 'green-endpoint',   
                        'Type': 'A',
                        'Weight': int(event['grWeight']),
                    },
                },
            ],
            'Comment': 'ELB load balancers for the api endpoint',
        },
        # Depends on the type of resource that you want to route traffic to
        HostedZoneId=R53_HOSTED_ZONE
        )
        request_id = response['ChangeInfo']['Id']
        message = "request_id: " + request_id
        send_message = slack_client.chat_postMessage(
            channel = SLACK_CHANNEL,
            text = message
        )
        assert send_message["message"]["text"] != ''
        return logger.info("request id: {}".format(request_id))
    except botocore.exceptions.ClientError as e:
        return logger.error("Boto3 ClientError: {}".format(e))
    

