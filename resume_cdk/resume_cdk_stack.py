from aws_cdk import (
    core, aws_ec2 as ec2,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cpactions, aws_codecommit as codecommit,
    aws_codebuild as codebuild, aws_s3 as s3,
    aws_s3_deployment as s3_deploy, pipelines,
    aws_route53 as route53, aws_route53_targets as route53_targets,
    aws_cloudfront as cdf, aws_cloudfront_origins as cdf_origins,
    aws_certificatemanager as certmgr, aws_lambda as lmb, 
    aws_dynamodb as dynamo, aws_apigateway as apigw
)

class ResumeCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # certificate = certmgr.DnsValidatedCertificate(self, 
        #     'HostedZoneCertificate',
        #     hosted_zone=hosted_zone,
        #     domain_name='untermuller.ch',
        #     region='us-east-1',
        #     subject_alternative_names=['resume.untermuller.ch','www.resume.untermuller.ch','www.untermuller.ch']
        #     )

        # website_bucket_create = s3.Bucket(self, 'WebsiteBucketCDK',
        #     bucket_name='BUCKET_NAME',
        #     website_index_document='index.html',
        #     website_error_document='error.html',
        #     public_read_access=True)

        table = dynamo.Table(
            self, 'HitCounter',
            partition_key={'name': 'id', 'type': dynamo.AttributeType.STRING}
        )

        counter = lmb.Function(self, 'CounterHandler',
            runtime=lmb.Runtime.PYTHON_3_8,
            handler='counter.lambda_handler',
            code=lmb.Code.asset('resume_cdk/lambda'),
            environment={
                'TABLE_NAME': table.table_name},
            )

        lambdaapigw = apigw.LambdaRestApi(self, 'Endpoint',
            handler=counter)

        endpoint = core.CfnOutput(self, 'ApiEndpoint', value=lambdaapigw.url)

        table.grant_read_write_data(counter)

        website_bucket = s3.Bucket.from_bucket_name(
            self,'BUCKET_NAME', 
            bucket_name='BUCKET_NAME')

        deploy_website = s3_deploy.BucketDeployment(
            self, 'DeployWebsiteCDK',
            sources=[s3_deploy.Source.asset("./website")],
            destination_bucket=website_bucket)

        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, 'HOST.CH', 
            hosted_zone_id='HOST_ID',
            zone_name='HOST.CH')

        certificate = certmgr.Certificate.from_certificate_arn(
            self, 'CERT_HOST.CH', 
            'CERT_HOST.CH_ARN')

        cdf_OAI = cdf.OriginAccessIdentity(self, 'OAI-user-s3', comment='OAI')
        
        grant_access = website_bucket.grant_read(cdf_OAI.grant_principal)

        s3_origin = cdf.S3OriginConfig(
            s3_bucket_source=website_bucket,
            origin_access_identity=cdf_OAI,
        )
        
        cdf_viewer_policy = cdf.ViewerProtocolPolicy('REDIRECT_TO_HTTPS')

        cdf_behavior = cdf.Behavior(is_default_behavior=True)
        
        cdf_source_config = cdf.SourceConfiguration(
            behaviors=[cdf_behavior],
            s3_origin_source=s3_origin,
        )

        cdf_dist = cdf.CloudFrontWebDistribution(
            self, 'ResumeDistribution',
            origin_configs=[cdf_source_config],
            viewer_certificate=cdf.ViewerCertificate.from_acm_certificate(
                certificate, 
                aliases=['HOST.CH', 'ALIAS_HOST.CH'],
                security_policy=cdf.SecurityPolicyProtocol.TLS_V1,
                ssl_method=cdf.SSLMethod.SNI
                ),
            viewer_protocol_policy=cdf_viewer_policy
        )

        route_Aname = route53.ARecord(
            self, 'ANAME', 
            record_name='HOST.CH', 
            target=route53.RecordTarget.from_alias(route53_targets.CloudFrontTarget(cdf_dist)),
            zone=hosted_zone, 
            comment="insert a record")