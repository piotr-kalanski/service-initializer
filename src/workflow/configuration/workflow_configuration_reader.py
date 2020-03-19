import yaml
from workflow.configuration.workflow_configuration import WorkflowConfiguration
from workflow.step import Step

from tasks.aws.codecommit import *
from tasks.aws.codepipeline import *
from tasks.aws.ecr import *
from tasks.git import Git_PushToRepository_Task

class WorkflowConfigurationReader:

    TASKS_CLASSES = {
        "AWS/CodeCommit/CreateRepository": AWS_CodeCommit_CreateRepository_Task,
        "AWS/CodePipeline/CreatePipeline": AWS_CodePipeline_CreatePipeline_Task,
        "AWS/ECR/CreateRepository": AWS_ECR_CreateRepository_Task,
        "git/PushToRepository": Git_PushToRepository_Task,
    }

    def read(self, file: str) -> WorkflowConfiguration:
        configuration_content = yaml.load(open(file))
        wc = WorkflowConfiguration()

        for s in configuration_content['steps']:
            step_name = s['name']
            task_type = s['task']['type']

            step = Step(
                name=step_name,
                task=self.TASKS_CLASSES[task_type]()
            )
            wc.add_step(step)

        return wc
