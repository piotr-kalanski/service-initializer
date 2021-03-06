import unittest
import pytest
import os
from workflow.configuration.workflow_configuration_reader import WorkflowConfigurationReader
from workflow.configuration.exceptions import NotExistingTaskException

from tasks.aws.codecommit import AWS_CodeCommit_CreateRepository_Task
from tasks.aws.codepipeline import AWS_CodePipeline_CreatePipeline_Task
from tasks.aws.ecr import AWS_ECR_CreateRepository_Task
from tasks.git import Git_PushToRepository_Task

class TestWorkflowConfigurationReader(unittest.TestCase):

    workflow_configuration_reader: WorkflowConfigurationReader

    def setUp(self):
        self.workflow_configuration_reader = WorkflowConfigurationReader()

    def test_read_simple_config(self):
        wc = self.workflow_configuration_reader.read("test/workflows/workflow_simple.yaml")

        steps = wc.get_steps()

        self.assertEqual("Step1", steps[0].name)
        self.assertEqual("Step2", steps[1].name)
        self.assertEqual("Step3", steps[2].name)

        self.assertEqual(AWS_CodeCommit_CreateRepository_Task, steps[0].task.__class__)
        self.assertEqual(AWS_CodePipeline_CreatePipeline_Task, steps[1].task.__class__)
        self.assertEqual(AWS_ECR_CreateRepository_Task, steps[2].task.__class__)

    def test_read_workflow_with_not_existing_task(self):
        with pytest.raises(NotExistingTaskException):
            self.workflow_configuration_reader.read("test/workflows/workflow_with_not_existing_task.yaml")

    def test_read_workflow_with_secrets(self):
        os.environ['ENVIRONMENT_VARIABLE'] = 'SECRET_VALUE'

        wc = self.workflow_configuration_reader.read("test/workflows/workflow_with_secrets.yaml")

        steps = wc.get_steps()
        task = steps[0].task

        self.assertEqual('SECRET_VALUE', task.auth_token)
        self.assertEqual('value1', task.service_metadata_parameter_with_request_body)
