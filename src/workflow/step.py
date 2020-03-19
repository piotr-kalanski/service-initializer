import logging
from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata


class Step:

    def __init__(self, name: str, task: AbstractTask):
        self.name = name
        self.task = task

    def run(self, service_metadata: ServiceMetadata):
        logging.info(f"Running step {self.name}")
        self.task.execute(service_metadata)
