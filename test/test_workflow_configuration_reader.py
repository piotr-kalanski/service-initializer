import unittest
from workflow.configuration.workflow_configuration_reader import WorkflowConfigurationReader


class TestWorkflowConfigurationReader(unittest.TestCase):

    workflow_configuration_reader: WorkflowConfigurationReader

    def setUp(self):
        self.workflow_configuration_reader = WorkflowConfigurationReader()

    def test_read_simple_config_only_step_names(self):
        wc = self.workflow_configuration_reader.read("test/workflows/workflow_simple.yaml")

        steps = wc.get_steps()

        self.assertEqual("Step1", steps[0].name)
        self.assertEqual("Step2", steps[1].name)
