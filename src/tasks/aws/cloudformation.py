import logging
import boto3
from typing import List
from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata


class AWS_CloudFormation_CreateStack_Task(AbstractTask):
    
    def __init__(
        self,
        template_body: str,
        service_metadata_parameter_with_stack_name: str,
        stack_parameters: dict = {},
        service_metadata_parameter_with_stack_parameters: str = '',
    ):
        self.template_body = template_body
        self.stack_parameters = stack_parameters
        self.service_metadata_parameter_with_stack_name = service_metadata_parameter_with_stack_name
        self.service_metadata_parameter_with_stack_parameters = service_metadata_parameter_with_stack_parameters

    def execute(self, service_metadata: ServiceMetadata):
        logging.info("Creating AWS CloudFormation stack")
        client = boto3.client('cloudformation') 

        stack_name = self._get_stack_name()

        response = client.create_stack(
            StackName=stack_name,
            TemplateBody=self.template_body,
            Parameters=self._get_stack_parameters(),
        )
        
        logging.info(f"AWS CloudFormation stack '{stack_name}' created")

    def _get_stack_name(self, service_metadata: ServiceMetadata) -> str:
        return service_metadata.parameters[self.service_metadata_parameter_with_stack_name]

    def _get_stack_parameters(self, service_metadata: ServiceMetadata) -> List[dict]:
        if self.service_metadata_parameter_with_stack_parameters:
            merged_params = {
                **self.stack_parameters,
                **service_metadata.parameters[self.service_metadata_parameter_with_stack_parameters]
            }
        else:
            merged_params = self.stack_parameters

        return [
            {
                'ParameterKey': item[0],
                'ParameterValue': item[1],
            }
            for item in merged_params.items()
        ]
