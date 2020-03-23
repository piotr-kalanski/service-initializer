import logging
import git
from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata


class Git_CloneRepository_Task(AbstractTask):

    def __init__(
        self,
        service_metadata_parameter_with_target_directory: str,
        service_metadata_parameter_with_repository_url: str,
    ):
       self.service_metadata_parameter_with_target_directory = service_metadata_parameter_with_target_directory
       self.service_metadata_parameter_with_repository_url = service_metadata_parameter_with_repository_url


    def execute(self, service_metadata: ServiceMetadata):
        logging.info("Cloning git repository")
        target_directory = service_metadata.parameters[self.service_metadata_parameter_with_target_directory]
        repository_url = service_metadata.parameters[self.service_metadata_parameter_with_repository_url]
        git.Git(target_directory).clone(repository_url)
        logging.info(f"Cloned git repository {repository_url} to directory {target_directory}")


# TODO - implementation - this is only template
class Git_PushToRepository_Task(AbstractTask):
    
#    def __init__(self):
        

    def execute(self, service_metadata: ServiceMetadata):
        logging.info("Pushing to git repository")
        # TODO - implementation
