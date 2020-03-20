import logging
import boto3
from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata


class AWS_CodeCommit_CreateRepository_Task(AbstractTask):
    
    # def __init__(self):

    def execute(self, service_metadata: ServiceMetadata):
        logging.info("Creating AWS Code Commit repository")
        client = boto3.client('codecommit')      
        response = client.create_repository(
            repositoryName=service_metadata.name,
            repositoryDescription=service_metadata.description
        )
        repository_name = response['repositoryMetadata']['repositoryName']
        logging.info(f"AWS Code Commit repository '{repository_name}' created")
