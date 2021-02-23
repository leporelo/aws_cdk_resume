from aws_cdk import (
    core, 
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cpactions,
    aws_codecommit as codecommit,
    aws_s3 as s3,
    pipelines
)

from resume_cdk.resume_cdk_stack import ResumeCdkStack
from resume_cdk.resume_build import ResumeBuildStack

class ResumeDeployStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        ResumeCdkStack(self, 'deploy-website-to-s3')

class ResumeBuildStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        ResumeBuildStack(self, 'build-website')