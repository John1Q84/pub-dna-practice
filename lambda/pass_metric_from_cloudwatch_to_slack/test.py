
import boto3
import botocore
import json
import logging
import os
import requests


#SLACK_CHANNEL = os.environ['slackChannel']
#HOOK_URL = os.environ['hookUrl']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('cloudwatch')
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
        "width": 967,
        "height": 250,
        "start": "-PT1H",
        "end": "P0D" 
    }
]



def get_metric_image():    
    metric_data=json.dumps(metric_source[0])    
    print ("metric_data: ", metric_data)
    print ("metric_data type = ", type(metric_data))
    image_data = client.get_metric_widget_image(
        MetricWidget=metric_data,
        OutputFormat='png'
    )
