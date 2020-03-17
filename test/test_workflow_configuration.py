import unittest
from workflow.configuration.workflow_configuration import WorkflowConfiguration
from workflow.step import Step
from dummy_task import DummyTask


class TestWorkflowConfiguration(unittest.TestCase):

    workflow_configuration: WorkflowConfiguration

    def setUp(self):
        self.workflow_configuration = WorkflowConfiguration()

    def test_add_step(self):
        s1 = Step("Step1", DummyTask())
        s2 = Step("Step2", DummyTask())

        self.workflow_configuration.add_step(s1)
        self.workflow_configuration.add_step(s2)

        steps = self.workflow_configuration.get_steps()

        self.assertEqual(s1, steps[0])
        self.assertEqual(s2, steps[1])
