
from abc import ABC
from abc import abstractmethod
from workflow.service_metadata import ServiceMetadata


class AbstractTask:
    
    @abstractmethod
    def execute(self, service_metadata: ServiceMetadata):
        ...
