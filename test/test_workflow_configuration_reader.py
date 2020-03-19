import unittest
from workflow.configuration.workflow_configuration_reader import WorkflowConfigurationReader

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
        self.assertEqual("Step4", steps[3].name)

        self.assertEqual(AWS_CodeCommit_CreateRepository_Task, steps[0].task.__class__)
        self.assertEqual(AWS_CodePipeline_CreatePipeline_Task, steps[1].task.__class__)
        self.assertEqual(AWS_ECR_CreateRepository_Task, steps[2].task.__class__)
        self.assertEqual(Git_PushToRepository_Task, steps[3].task.__class__)
