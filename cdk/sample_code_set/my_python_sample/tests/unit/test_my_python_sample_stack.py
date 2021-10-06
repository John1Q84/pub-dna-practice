import json
import pytest

from aws_cdk import core
from my_python_sample.my_python_sample_stack import MyPythonSampleStack


def get_template():
    app = core.App()
    MyPythonSampleStack(app, "my-python-sample")
    return json.dumps(app.synth().get_stack("my-python-sample").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
