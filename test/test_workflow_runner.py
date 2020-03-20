import unittest
from workflow.configuration.workflow_configuration import WorkflowConfiguration
from workflow.step import Step
from workflow.runner import WorkflowRunner
from dummy_task import DummyTask
from service_metadata.model import ServiceMetadata


class TestWorkflowExecutor(unittest.TestCase):

    workflow_runner: WorkflowRunner

    def setUp(self):
        self.workflow_runner = WorkflowRunner()

    def test_run_workflow(self):
        workflow_configuration = WorkflowConfiguration()
        t1 = DummyTask()
        t2 = DummyTask()
        s1 = Step("Step1", t1)
        s2 = Step("Step2", t2)
        workflow_configuration.add_step(s1)
        workflow_configuration.add_step(s2)

        metadata = ServiceMetadata(
            name="name",
            description="description",
            parameters={
                "key": "value"
            }
        )

        self.workflow_runner.run(workflow_configuration, metadata)

        self.assertTrue(t1.executed)
        self.assertEqual(t1.service_metadata, metadata)
        self.assertTrue(t2.executed)
        self.assertEqual(t2.service_metadata, metadata)
