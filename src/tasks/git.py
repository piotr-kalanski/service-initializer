import logging
import git
from git import Repo
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


class Git_PushToRepository_Task(AbstractTask):
    
    COMMIT_MESSAGE = 'Service Initializer commit'

    def __init__(self, service_metadata_parameter_with_path_of_git_repository: str):
        self.service_metadata_parameter_with_path_of_git_repository = service_metadata_parameter_with_path_of_git_repository

    def execute(self, service_metadata: ServiceMetadata):
        logging.info("Pushing new files to git repository")
        
        path_of_git_repo = service_metadata.parameters[self.service_metadata_parameter_with_path_of_git_repository] + '/.git'

        repo = Repo(path_of_git_repo)
        repo.git.add('.')
        repo.index.commit(self.COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()

        logging.info("Pushed new files to git repository")
