#!/usr/bin/env python3

from aws_cdk import core

from my_python_sample.my_python_sample_stack import MyPythonSampleStack


app = core.App()
MyPythonSampleStack(app, "my-python-sample", env={'region': 'us-west-2'})

app.synth()
