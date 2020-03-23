import logging
import os
from typing import List
from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata


class Docker_Run_Task(AbstractTask):
    
    def __init__(self, docker_image: str, task_parameters: dict, docker_run_options: List[str]=[]):
        self.docker_image = docker_image
        self.task_parameters = task_parameters
        self.docker_run_options = docker_run_options

    def execute(self, service_metadata: ServiceMetadata):
        options = ''
        for option in self.docker_run_options:
            options += option + ' '

        command = f"docker run -it --rm {options}{self.docker_image}" \
                f" --name {service_metadata.name}" \
                f' --description "{service_metadata.description}"' \
                f' --parameters "{str(self.task_parameters)}"' \
                f' --service-metadata "{str(service_metadata.parameters)}"'
        logging.info(f"Executing command: {command}")
        os.system(command)
