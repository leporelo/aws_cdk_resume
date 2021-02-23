#!/usr/bin/env python3

from aws_cdk import core

from resume_cdk.resume_cdk_stack import ResumeCdkStack
from resume_cdk.resume_pipeline import ResumePipeline


app = core.App()
ResumePipeline(app, "ResumeCdk")

app.synth()
