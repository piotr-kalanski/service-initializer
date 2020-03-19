import logging
import boto3
from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata


class AWS_ECR_CreateRepository_Task(AbstractTask):
    
#    def __init__(self):
        

    def execute(self, service_metadata: ServiceMetadata):
        logging.info("Creating AWS ECR repository")
        client = boto3.client('ecr')
        repository_name = service_metadata.name
        # based on: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Client.create_repository
        response = client.create_repository(
            repositoryName=repository_name,
        )
        logging.info(f"AWS ECR repository '{repository_name}' created")
