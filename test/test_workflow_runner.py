import unittest
from workflow.configuration.workflow_configuration import WorkflowConfiguration
from workflow.step import Step
from workflow.runner import WorkflowRunner
from dummy_task import DummyTask


class TestWorkflowExecutor(unittest.TestCase):

    workflow_runner: WorkflowRunner

    def setUp(self):
        self.workflow_runner = WorkflowRunner()

    def test_execute_workflow(self):
        workflow_configuration = WorkflowConfiguration()
        t1 = DummyTask()
        t2 = DummyTask()
        s1 = Step("Step1", t1)
        s2 = Step("Step2", t2)
        workflow_configuration.add_step(s1)
        workflow_configuration.add_step(s2)

        self.workflow_runner.run(workflow_configuration)

        self.assertTrue(t1.executed)
        self.assertTrue(t2.executed)
