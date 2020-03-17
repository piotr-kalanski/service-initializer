import logging
from workflow.configuration.workflow_configuration import WorkflowConfiguration


class WorkflowRunner:

    def run(self, workflow_configuration: WorkflowConfiguration):
        logging.info("Workflow started")
        for step in workflow_configuration.get_steps():
            step.run()
        logging.info("Workflow finished")
