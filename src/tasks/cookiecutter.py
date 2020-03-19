from cookiecutter.main import cookiecutter
from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata

# TODO - implementation - this is only template
class Cookiecutter_GenerateProjectDirectory_Task(AbstractTask):

#    def __init__(self):
        

    def execute(self, service_metadata: ServiceMetadata):
        logging.info("Generating project directory using cookiecutter")
        # TODO - implementation
        template_url = "" # TODO
        parameters = {} # TODO
        output_dir = '' # TODO
        
        cookiecutter(
            template=template_url,
            no_input=True,
            extra_context=parameters,
            output_dir=output_dir,
        )
        logging.info("Generated project directory using cookiecutter")

