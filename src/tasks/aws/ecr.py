import logging
from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata

# TODO - implementation - this is only template
class AWS_ECR_CreateRepository_Task(AbstractTask):
    
#    def __init__(self):
        

    def execute(self, service_metadata: ServiceMetadata):
        logging.info("Creating AWS ECR repository")
        # TODO - implementation
