import yaml
from workflow.configuration.workflow_configuration import WorkflowConfiguration
from workflow.step import Step
from workflow.configuration.exceptions import NotExistingTaskException

from tasks.aws.codecommit import *
from tasks.aws.codepipeline import *
from tasks.aws.ecr import *
from tasks.aws.cloudformation import *
from tasks.git import Git_PushToRepository_Task
from tasks.cookiecutter import Cookiecutter_GenerateProjectDirectory_Task

class WorkflowConfigurationReader:

    # dictionary mapping task name used in YAML file with workflow configuration to Python for specific Task class
    TASKS_CLASSES = {
        "AWS/CodeCommit/CreateRepository": AWS_CodeCommit_CreateRepository_Task,
        "AWS/CodePipeline/CreatePipeline": AWS_CodePipeline_CreatePipeline_Task,
        "AWS/ECR/CreateRepository": AWS_ECR_CreateRepository_Task,
        "AWS/CloudFormation/CreateStack": AWS_CloudFormation_CreateStack_Task,
        "git/PushToRepository": Git_PushToRepository_Task,
        'Cookiecutter/GenerateProjectDirectory': Cookiecutter_GenerateProjectDirectory_Task,
    }

    def read(self, file: str) -> WorkflowConfiguration:
        configuration_content = yaml.load(open(file), Loader=yaml.FullLoader)
        wc = WorkflowConfiguration()

        for s in configuration_content['steps']:
            step_name = s['name']
            task = s['task']
            task_type = task['type']
            task_parameters = task['parameters'] if 'parameters' in task else {}

            if task_type not in self.TASKS_CLASSES:
                raise NotExistingTaskException()

            step = Step(
                name=step_name,
                task=self.TASKS_CLASSES[task_type](**task_parameters)
            )
            wc.add_step(step)

        return wc
