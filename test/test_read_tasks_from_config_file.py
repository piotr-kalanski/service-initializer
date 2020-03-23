import unittest
from workflow.configuration.workflow_configuration_reader import WorkflowConfigurationReader

from tasks.aws.codecommit import AWS_CodeCommit_CreateRepository_Task
from tasks.aws.codepipeline import AWS_CodePipeline_CreatePipeline_Task
from tasks.aws.ecr import AWS_ECR_CreateRepository_Task
from tasks.aws.cloudformation import AWS_CloudFormation_CreateStack_Task
from tasks.git import *
from tasks.github import GitHub_CreateRepository_Task
from tasks.docker import Docker_Run_Task
from tasks.cookiecutter import Cookiecutter_GenerateProjectDirectory_Task


class TestReadingTasksFromConfigFile(unittest.TestCase):

    workflow_configuration_reader: WorkflowConfigurationReader

    def setUp(self):
        self.workflow_configuration_reader = WorkflowConfigurationReader()

    def test_read_aws_codecommit_createrepository_task(self):
        task = self.__get_first_task_from_workflow_at("test/workflows/aws_codecommit_createrepository_task.yaml")
        
        self.assertEqual(AWS_CodeCommit_CreateRepository_Task, task.__class__)

    def test_read_aws_ecr_createrepository_task(self):
        task = self.__get_first_task_from_workflow_at("test/workflows/aws_ecr_createrepository_task.yaml")
        
        self.assertEqual(AWS_ECR_CreateRepository_Task, task.__class__)

    def test_read_aws_cloudformation_createstack_task_basic(self):
        task = self.__get_first_task_from_workflow_at("test/workflows/aws_cloudformation_createstack_task-basic.yaml")
        
        self.assertEqual(AWS_CloudFormation_CreateStack_Task, task.__class__)
        self.assertEqual('cf_stack_name', task.service_metadata_parameter_with_stack_name)
        self.assertEqual("""
            Resources:
                S3Bucket:
                Type: AWS::S3::Bucket
                DeletionPolicy: Retain
                Properties:
                    BucketName: my-bucket
            """.strip().replace(' ', ''),
            task.template_body.strip().replace(' ', '')
        )

    def test_read_aws_cloudformation_createstack_task_with_parameters(self):
        task = self.__get_first_task_from_workflow_at("test/workflows/aws_cloudformation_createstack_task-with_parameters.yaml")
        
        self.assertEqual(AWS_CloudFormation_CreateStack_Task, task.__class__)
        self.assertEqual('cf_stack_name', task.service_metadata_parameter_with_stack_name)
        self.assertEqual("""
            Resources:
                S3Bucket:
                Type: AWS::S3::Bucket
                DeletionPolicy: Retain
                Properties:
                    BucketName: my-bucket
            """.strip().replace(' ', ''),
            task.template_body.strip().replace(' ', '')
        )
        self.assertEqual({'p1':'v1', 'p2':'v2'}, task.stack_parameters)
        self.assertEqual('cf_stack_parameters', task.service_metadata_parameter_with_stack_parameters)

    def test_read_github_createrepository_task(self):
        task = self.__get_first_task_from_workflow_at("test/workflows/github_createrepository_task.yaml")
        
        self.assertEqual(GitHub_CreateRepository_Task, task.__class__)
        self.assertEqual('TOKEN', task.auth_token)
        self.assertEqual('create_github_repository_body', task.service_metadata_parameter_with_request_body)

    def test_read_docker_run_task(self):
        task = self.__get_first_task_from_workflow_at("test/workflows/docker_run_task.yaml")
        self.assertEqual(Docker_Run_Task, task.__class__)
        self.assertEqual('piotrkalanski/service-initializer-cookiecutter-task', task.docker_image)
        self.assertEqual(
            {
                'template_url_field_name':'template_url',
                'output_dir':'/output/',
                'parameters_field_name':'params'
            },
            task.task_parameters
        )
        self.assertEqual([
                '-v dir1:dir2',
                'option2',
                'option3',
            ],
            task.docker_run_options
        )

    def test_read_cookiecutter_generateprojectdirectory_task(self):
        task = self.__get_first_task_from_workflow_at("test/workflows/cookiecutter_generateprojectdirectory_task.yaml")
        
        self.assertEqual(Cookiecutter_GenerateProjectDirectory_Task, task.__class__)
        self.assertEqual('piotrkalanski/service-initializer-cookiecutter-task', task.docker_image)
        self.assertEqual(
            {
                'template_url_field_name': 'template_url',
                'output_dir':'/output/',
                'parameters_field_name': 'cookiecutter_parameters',
            },
            task.task_parameters
        )
        self.assertEqual([
                '-v /tmp/output/:/output',
            ],
            task.docker_run_options
        )

    def test_read_git_clonerepository_task(self):
       task = self.__get_first_task_from_workflow_at("test/workflows/git_clonerepository_task.yaml")
       self.assertEqual(Git_CloneRepository_Task, task.__class__)
       self.assertEqual('target_directory', task.service_metadata_parameter_with_target_directory)
       self.assertEqual('repository_url', task.service_metadata_parameter_with_repository_url)

    def test_read_git_pushtorepository_task(self):
       task = self.__get_first_task_from_workflow_at("test/workflows/git_pushtopository_task.yaml")
       self.assertEqual(Git_PushToRepository_Task, task.__class__)
       self.assertEqual('path_of_git_repository', task.service_metadata_parameter_with_path_of_git_repository)

    def __get_first_task_from_workflow_at(self, file: str):
        wc = self.workflow_configuration_reader.read(file)
        steps = wc.get_steps()
        return steps[0].task
