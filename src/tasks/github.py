import logging
import requests
from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata

class GitHub_CreateRepository_Task(AbstractTask):

    GITHUB_BASE_URL = 'https://api.github.com'
    
    def __init__(
        self,
        auth_token: str,
        service_metadata_parameter_with_request_body: str,
    ):
        self.auth_token = auth_token
        self.service_metadata_parameter_with_request_body = service_metadata_parameter_with_request_body

    def execute(self, service_metadata: ServiceMetadata):
        logging.info("Creating GitHub repository")
        response = requests.post(
            url=self.GITHUB_BASE_URL + '/user/repos',
            json=service_metadata.parameters[self.service_metadata_parameter_with_request_body],
            headers={
                'Authorization': f"token {self.auth_token}"
            }
        )

        response_json = response.json()
        if response.status_code == 201:
            logging.info(f"GitHub repository {response_json['html_url']} created")
        else:
            logging.error("Error with creating GitHub repository: " + str(response_json))
