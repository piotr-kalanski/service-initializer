import yaml
from workflow.configuration.workflow_configuration import WorkflowConfiguration
from workflow.step import Step


class WorkflowConfigurationReader:

    def read(self, file: str) -> WorkflowConfiguration:
        content = yaml.load(open(file))
        wc = WorkflowConfiguration()

        for s in content['steps']:
            step = Step(
                name=s['name'],
                task=None # TODO - create task based on config
            )
            wc.add_step(step)

        return wc
