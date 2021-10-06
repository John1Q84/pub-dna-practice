from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import boto3, botocore
import logging
import os
import json
import time


logger = logging.getLogger()
logger.setLevel(logging.INFO)

CLUSTER_NAME = "myEcsCluster"

client = boto3.client('ecs')
'''

## request sample
response = client.update_service(
    cluster='string',
    service='string',
    desiredCount=123,
    taskDefinition='string',
    capacityProviderStrategy=[
        {
            'capacityProvider': 'string',
            'weight': 123,
            'base': 123
        },
    ],
    deploymentConfiguration={
        'deploymentCircuitBreaker': {
            'enable': True|False,
            'rollback': True|False
        },
        'maximumPercent': 123,
        'minimumHealthyPercent': 123
    },
    networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': [
                'string',
            ],
            'securityGroups': [
                'string',
            ],
            'assignPublicIp': 'ENABLED'|'DISABLED'
        }
    },
    placementConstraints=[
        {
            'type': 'distinctInstance'|'memberOf',
            'expression': 'string'
        },
    ],
    placementStrategy=[
        {
            'type': 'random'|'spread'|'binpack',
            'field': 'string'
        },
    ],
    platformVersion='string',
    forceNewDeployment=True|False,
    healthCheckGracePeriodSeconds=123,
    enableExecuteCommand=True|False
)
'''


def lambda_handler(event, context):
    
    try:
        response = client.update_service(
            cluster=CLUSTER_NAME,
            service=event['serviceName'],
            desiredCount=int(event['desireCount']),
            deploymentConfiguration={
                'deploymentCircuitBreaker': {
                    'enable': True,
                    'rollback': True
                },
                'maximumPercent': 200,
                'minimumHealthyPercent': 50
            },
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [
                        'subnet-0b7a16645e1a03e22',
                        'subnet-095a1f9d530a33240'
                    ],
                    'securityGroups': [
                        'sg-017e5fb56e3a4b99c'
                    ],
                    'assignPublicIp': 'DISABLED'
                }
            },
            platformVersion='LATEST',
            forceNewDeployment=True,
            healthCheckGracePeriodSeconds=10             
        )
        logger.info(response)
        # timer set as 180sec. If it is over, will get lambda task timed out error
        for i in range(1, 18):
            deploy_status = desc_ecs_service(CLUSTER_NAME, event['serviceName'])
            if deploy_status != "IN_PROGRESS":
                break
            time.sleep(10)
            i+=1

        if deploy_status == "COMPLETED":
            return logger.info("ECS service update is completed!")
        else:
            return logger.error("ECS service update failed!")
            
    except botocore.exceptions.ClientError as e:
        return logger.error("Boto3 ClientError: {}".format(e))


def desc_ecs_service(clusterName, serviceName):
    
    response = client.describe_services(
         cluster = clusterName,
         services = [serviceName]
    )
    #logger.info(response)
    rollout = response['services'][0]['deployments'][0]['rolloutState']
    return rollout

        
