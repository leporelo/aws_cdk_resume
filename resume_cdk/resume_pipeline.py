from aws_cdk import (
    core, 
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cpactions,
    aws_codecommit as codecommit,
    aws_s3 as s3,
    pipelines
)
# from .deploy_to_s3.deploy_website_stage import DeployToS3Stage
# from .deploy_to_s3.deploy_website import DeployToS3
from resume_cdk.resume_deploy_stage import (
    ResumeDeployStage, ResumeBuildStage
)

class ResumePipeline(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact('SourceArtifact')
        cloud_assembly_artifact = codepipeline.Artifact('CloudAssembly')

        resume_stack_repository = codecommit.Repository.from_repository_name(
            self, "ResumeStack",repository_name="ResumeStack")

        pipeline = pipelines.CdkPipeline(
            self, 'Pipeline',
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name="ResumeStack",
            source_action=cpactions.CodeCommitSourceAction(
                action_name='GetCodeCommit',
                output=source_artifact,
                repository=resume_stack_repository,
                trigger=cpactions.CodeCommitTrigger.POLL
                ),
            
            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                action_name='SimpleSynthAction',
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command='npm install -g aws-cdk && pip install -r requirements.txt',
                synth_command='cdk synth'))

        build_stage = pipeline.add_application_stage(ResumeBuildStage(self, 'BuildWebsite'))
        deploy_stage = pipeline.add_application_stage(ResumeDeployStage(self, 'Website'))
        