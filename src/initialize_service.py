import click
import json
import logging
from workflow.runner import WorkflowRunner
from workflow.configuration.workflow_configuration_reader import WorkflowConfigurationReader
from service_metadata.model import ServiceMetadata
from service_metadata.reader import ServiceMetadataReader


@click.command()
@click.option('--configuration', help='Path to workflow configuration YAML file.')
@click.option('--parameters', help='Path to YAML file with service parameters.')
def run(configuration, parameters):
    """Script initializing new service."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s %(message)s')

    workflow_runner = WorkflowRunner()
    workflow_configuration_reader = WorkflowConfigurationReader()
    service_metadata_reader = ServiceMetadataReader()

    workflow_configuration = workflow_configuration_reader.read(configuration)
    service_metadata = service_metadata_reader.read(parameters)

    workflow_runner.run(
        workflow_configuration=workflow_configuration,
        service_metadata=service_metadata
    )
    

if __name__ == '__main__':
    run()
