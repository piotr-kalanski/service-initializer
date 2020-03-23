import logging
from tasks.docker import Docker_Run_Task
from service_metadata.model import ServiceMetadata

class Cookiecutter_GenerateProjectDirectory_Task(Docker_Run_Task):

    def __init__(self, template_url_field_name: str, parameters_field_name: str, output_dir: str):
        super().__init__(
           docker_image='piotrkalanski/service-initializer-cookiecutter-task',
           task_parameters={
               'template_url_field_name': template_url_field_name,
               'output_dir': '/output/',
               'parameters_field_name': parameters_field_name
            },
            docker_run_options=[
                f'-v {output_dir}:/output'
            ]
        )
