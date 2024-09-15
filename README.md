# study-cdk-scheduled-containers
This is a sample project to study how to use the CDK to schedule containers.

There is an issue described [here](https://github.com/aws/aws-cdk/issues/26702) that you need to add additional options to the ScheduledFargateTask.

```python
# see: https://github.com/aws/aws-cdk/issues/26702
scheduled_fargate_task_definition_options = ecs_patterns.ScheduledFargateTaskDefinitionOptions(
    task_definition=self.task_definition,
)
```

# dev container
Use vscode with the dev container extension and then use CMD+SHIFT+P and choose either 'reopen in container' or 'rebuild container'.

# terminal
You can open a terminal by using CMD+SHIFT+P and choosing 'create new terminal' and you'll enter the container shell.

