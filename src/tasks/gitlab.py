import logging
import requests
from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata

class GitLab_CreateProject_Task(AbstractTask):

    GITLAB_BASE_URL = 'https://gitlab.com/api/v4'
    
    def __init__(
        self,
        personal_token: str,
        service_metadata_parameter_with_request_body: str,
    ):
        self.personal_token = personal_token
        self.service_metadata_parameter_with_request_body = service_metadata_parameter_with_request_body

    def execute(self, service_metadata: ServiceMetadata):
        logging.info("Creating GitLab project")
        response = requests.post(
            url=self.GITLAB_BASE_URL + '/projects',
            json=service_metadata.parameters[self.service_metadata_parameter_with_request_body],
            headers={
                'Private-Token': f"{self.personal_token}"
            }
        )

        response_json = response.json()
        logging.info(response_json)
        if response.status_code == 201:
            logging.info(f"GitLab project created")
        else:
            logging.error("Error with creating GitLab project: " + str(response_json))
