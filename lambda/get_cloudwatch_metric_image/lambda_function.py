from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


import boto3
import botocore
import json
import logging
import os
import requests


# The base-64 encoded, encrypted key (CiphertextBlob) stored in the kmsEncryptedHookUrl environment variable
# ENCRYPTED_HOOK_URL = os.environ['kmsEncryptedHookUrl']
# The Slack channel to send a message to stored in the slackChannel environment variable
SLACK_CHANNEL = os.environ['slackChannel']

# Get slack token from SSM Parameter Store
ssm = boto3.client('ssm')
SLACK_TOKEN = ssm.get_parameter(Name='SLACK_TOKEN', WithDecryption=True)['Parameter']['Value']


WIDTH = int(os.environ['image_width'])
HEIGHT = int(os.environ['image_height'])


logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = WebClient(token=SLACK_TOKEN)

cloudwatch = boto3.client('cloudwatch')
metric_source = [
    { 
        "metrics": [
            [ 
                "AWS/ApplicationELB", 
                "HealthyHostCount", 
                "TargetGroup", 
                "targetgroup/myAws-myTgb-1M9OUPT2TRQF8/eeae047ed044aef5", 
                "LoadBalancer", 
                "app/myAlb-blue/3eef135a611fb874" 
            ], 
            [ 
                ".",
                ".",
                ".", 
                "targetgroup/myAws-myTgg-F8WPCRQ9ASHM/47812d462b69c625",
                ".", 
                "app/myAlb-green/c3fc649b472e87b3", 
                { 
                    "color": "#2ca02c" 
                } 
            ]
        ],
        "view": "timeSeries",
        "stacked": False,
        "title": "[AVG] HealthyHost Count",
        "stat": "Average", 
        "period": 60, 
        "yAxis": 
        { 
            "right": 
            { 
                "min": 0 
            }, 
            "left": 
            {
                "min": 0 
            }
        },
        "liveData": True,
        "annotations": {
            "horizontal": [
                {
                    "color": "#d62728",
                    "label": "Alert Criteria",
                    "value": 1,
                    "fill": "below"
                }
            ]
        },
        "width": WIDTH,
        "height": HEIGHT,
        "start": "-PT1H",
        "end": "P0D" 
    }
]


def lambda_handler(event, context):
    print(SLACK_TOKEN)
    channel = SLACK_CHANNEL    
    metric_data = json.dumps(metric_source[0])
    image_data = cloudwatch.get_metric_widget_image(
        MetricWidget=metric_data,
        OutputFormat='png'
    )
    logger.info("channel: " + str(channel))
    logger.info("SLACK_TOKEN: " + SLACK_TOKEN)
    #image = {'file': image_data['MetricWidgetImage']}
    #logger.info("image: " + str(image))
    slack_params = {
        "filename": "metirc.png",
        "token": SLACK_TOKEN,  
        "channels": [channel]
    }
    logger.info("slack_param: " + str(slack_params))
    
    try:
        response = client.files_upload(
            channels=channel,
            file=image_data['MetricWidgetImage'],
            filetype="png",
            filename="metric.png",
            title="Cloudwatch Metric"
        )
        logger.info(response)
    except SlackApiError as e:
        logger.error("Error uploading file: {}".format(e))
