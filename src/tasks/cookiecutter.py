from cookiecutter.main import cookiecutter
from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata


class Cookiecutter_GenerateProjectDirectory_Task(AbstractTask):

    def __init__(self, template_url_field_name: str, parameters_field_name: str, output_dir: str):
        self.template_url_field_name = template_url_field_name
        self.parameters_field_name = parameters_field_name
        self.output_dir = output_dir

    def execute(self, service_metadata: ServiceMetadata):
        logging.info("Generating project directory using cookiecutter")

        template_url = service_metadata.parameters[self.template_url_field_name]
        parameters = service_metadata.parameters[self.parameters_field_name]
        output_dir = self.output_dir
        
        cookiecutter(
            template=template_url,
            no_input=True,
            extra_context=parameters,
            output_dir=output_dir,
        )

        logging.info("Generated project directory using cookiecutter")
