import click
import json
from workflow.runner import WorkflowRunner
from workflow.configuration.workflow_configuration_reader import WorkflowConfigurationReader
from workflow.service_metadata.model import ServiceMetadata


@click.command()
@click.option('--configuration', help='Path to workflow configuration YAML file.')
@click.option('--parameters', help='Path to YAML file with service parameters.')
def run(configuration, parameters):
    """Script initializing new service."""
    workflow_runner = WorkflowRunner()
    workflow_configuration_reader = WorkflowConfigurationReader()

    workflow_configuration = workflow_configuration_reader.read(configuration)
    service_metadata = # todo

    workflow_runner.run(
        workflow_configuration=workflow_configuration,
        service_metadata=service_metadata
    )
    

if __name__ == '__main__':
    run()
