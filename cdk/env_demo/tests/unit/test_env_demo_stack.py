import json
import pytest

from aws_cdk import core
from env_demo.env_demo_stack import EnvDemoStack


def get_template():
    app = core.App()
    EnvDemoStack(app, "env-demo")
    return json.dumps(app.synth().get_stack("env-demo").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
