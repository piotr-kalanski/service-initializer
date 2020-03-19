from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata


class DummyTask(AbstractTask):
    
    def __init__(self):
        self.executed = False
        self.service_metadata: ServiceMetadata

    def execute(self, service_metadata: ServiceMetadata):
        self.executed = True
        self.service_metadata = service_metadata
