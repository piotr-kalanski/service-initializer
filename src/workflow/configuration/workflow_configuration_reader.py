import yaml
from workflow.configuration.workflow_configuration import WorkflowConfiguration
from workflow.step import Step
from workflow.configuration.exceptions import NotExistingTaskException
from workflow.configuration.secrets_reader import SecretsReader

from tasks.aws.codecommit import *
from tasks.aws.codepipeline import *
from tasks.aws.ecr import *
from tasks.aws.cloudformation import *
from tasks.git import *
from tasks.github import GitHub_CreateRepository_Task
from tasks.gitlab import GitLab_CreateProject_Task
from tasks.cookiecutter import Cookiecutter_GenerateProjectDirectory_Task
from tasks.docker import Docker_Run_Task

class WorkflowConfigurationReader:

    # dictionary mapping task name used in YAML file with workflow configuration to Python for specific Task class
    TASKS_CLASSES = {
        "AWS/CodeCommit/CreateRepository": AWS_CodeCommit_CreateRepository_Task,
        "AWS/CodePipeline/CreatePipeline": AWS_CodePipeline_CreatePipeline_Task,
        "AWS/ECR/CreateRepository": AWS_ECR_CreateRepository_Task,
        "AWS/CloudFormation/CreateStack": AWS_CloudFormation_CreateStack_Task,
        "git/CloneRepository": Git_CloneRepository_Task,
        "git/PushToRepository": Git_PushToRepository_Task,
        'GitHub/CreateRepository': GitHub_CreateRepository_Task,
        'GitLab/CreateProject': GitLab_CreateProject_Task,
        'Cookiecutter/GenerateProjectDirectory': Cookiecutter_GenerateProjectDirectory_Task,
        'Docker/Run': Docker_Run_Task,
    }

    def read(self, file: str) -> WorkflowConfiguration:
        configuration_content = self.__read_configuration_file(file)
        secrets = self.__read_secrets(configuration_content)
        return self.__deserialize_workflow_configuration(
            steps=configuration_content['steps'],
            secrets=secrets,
        )

    def __read_configuration_file(self, file: str) -> dict:
        return yaml.load(open(file), Loader=yaml.FullLoader)

    def __read_secrets(self, configuration: dict) -> dict:
        if 'secrets' in configuration:
            s = configuration['secrets']
            secrets_reader = SecretsReader()

            return secrets_reader.read(
                environment_variables=s['environment'] if 'environment' in s else {},
                files=s['files'] if 'files' in s else []
            )
        else:
            return {}

    def __transform_parameters(self, parameters: dict, secrets: dict) -> dict:

        def transform_value(v) -> str:
            result = v

            if type(v) == str and v.startswith('{'):
                if v.startswith('{secret:'):
                    secret_key = v.replace('{secret:', '')[:-1]
                    result = secrets[secret_key]

            return result

        return {
            k:transform_value(v)
            for (k,v) in parameters.items()
        }

    def __deserialize_workflow_configuration(self, steps: List[dict], secrets: dict) -> WorkflowConfiguration:
        wc = WorkflowConfiguration()
        for s in steps:
            step_name = s['name']
            task = s['task']
            task_type = task['type']
            
            if task_type not in self.TASKS_CLASSES:
                raise NotExistingTaskException()

            task_parameters = task['parameters'] if 'parameters' in task else {}
            task_parameters = self.__transform_parameters(task_parameters, secrets)

            step = Step(
                name=step_name,
                task=self.TASKS_CLASSES[task_type](**task_parameters)
            )
            wc.add_step(step)

        return wc
