import logging
from workflow.configuration.workflow_configuration import WorkflowConfiguration
from workflow.service_metadata import ServiceMetadata


class WorkflowRunner:

    def run(self, workflow_configuration: WorkflowConfiguration, service_metadata: ServiceMetadata):
        logging.info("Workflow started")
        for step in workflow_configuration.get_steps():
            step.run(service_metadata)
        logging.info("Workflow finished")
