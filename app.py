import os
import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk import aws_logs as logs
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_iam as iam
from aws_cdk import aws_logs as logs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_applicationautoscaling as appscaling
import dotenv

dotenv.load_dotenv()



class ScheduledContainerStack(Stack):
    def __init__(self, scope: cdk.App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, id="vpc", vpc_id="vpc-3b95065c")

        selected_subnets = vpc.select_subnets(
            subnet_filters=[
                ec2.SubnetFilter.by_ids( subnet_ids=[
                    "subnet-cd5c51f0",
                    "subnet-ac8667e5",
                    "subnet-bf3c0d95",
                    ])
            ]
        )

        subnet_selection: ec2.SubnetSelection = ec2.SubnetSelection(
            subnets=selected_subnets.subnets
        )

        task_definition = ecs.FargateTaskDefinition(self, "FargateTaskDefinition")
        
        task_definition.add_container(
            id="scheduled_task", 
            image=ecs.ContainerImage.from_registry("python:3.12"),
            logging=ecs.LogDriver.aws_logs(
                stream_prefix="scheduled-tasks",
                log_group=logs.LogGroup(self, "ScheduledTaskLogGroup", log_group_name="my-scheduled-tasks"),
            )
        )

        task_definition.add_to_task_role_policy(
            iam.PolicyStatement(
                actions=[
                    "s3:GetObject",
                    "ecs:RunTask",
                ],
                resources=["*"])
        )
        
        task_definition.add_to_execution_role_policy(
            iam.PolicyStatement(
                actions=[
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:BatchGetImage",
                    "ecr:GetAuthorizationToken",
                    "ecr:GetDownloadUrlForLayer",
                    "ecs:DescribeTasks",
                    "ecs:ExecuteCommand",
                    "ecs:RunTask",
                    "ecs:StartTask",
                    "ecs:StopTask",
                    "ecs:UpdateService",
                    "kms:Decrypt",
                    "logs:*",
                    "secretsmanager:GetSecretValue",
                    "ssm:DescribeSessions",
                    "ssm:GetParameters",                    
                    "ssm:StartSession",
                ], 
                resources=["*"])
        )

        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc, cluster_name="my-scheduled-tasks")
        
        # see: https://github.com/aws/aws-cdk/issues/26702
        scheduled_fargate_task_definition_options = ecs_patterns.ScheduledFargateTaskDefinitionOptions(
            task_definition=task_definition,
        )

        scheduled_fargate_task = ecs_patterns.ScheduledFargateTask(self, "ScheduledFargateTask",
            cluster=cluster,            
            schedule=appscaling.Schedule.expression("rate(1 minute)"),
            subnet_selection = subnet_selection,
            scheduled_fargate_task_definition_options=scheduled_fargate_task_definition_options,
        )

app = cdk.App()
# set the environment
env = cdk.Environment(account=os.getenv('AWS_ACCOUNT'), region=os.getenv('AWS_REGION'))
# create the stack
ScheduledContainerStack(app, "ScheduledContainerStack", env=env)
# synthesize the CFN template
app.synth()
