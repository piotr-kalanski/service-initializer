import unittest
from configuration.workflow_configuration import WorkflowConfiguration


class TestWorkflowConfiguration(unittest.TestCase):

    workflow_configuration: WorkflowConfiguration

    def setUp(self):
        self.workflow_configuration = WorkflowConfiguration()

    def test_dummy(self):
        self.assertTrue(True)
