import logging
import boto3
from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata


class AWS_CodeCommit_CreateRepository_Task(AbstractTask):
    
    def __init__(self):
        self.client = boto3.client('codecommit')      

    def execute(self, service_metadata: ServiceMetadata):
        logging.info("Creating AWS Code Commit repository")
        response = self.client.create_repository(
            repositoryName=service_metadata.name,
            repositoryDescription=service_metadata.description
        )
        repository_name = response['repositoryName']
        logging.info(f"AWS Code Commit repository '{repository_name}' created")
