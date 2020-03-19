
from abc import ABC
from abc import abstractmethod
from service_metadata.model import ServiceMetadata


class AbstractTask:
    
    @abstractmethod
    def execute(self, service_metadata: ServiceMetadata):
        ...
