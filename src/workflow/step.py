import logging
from tasks.abstract_task import AbstractTask
from workflow.service_metadata import ServiceMetadata


class Step:

    def __init__(self, name: str, task: AbstractTask):
        self._name = name
        self._task = task

    def run(self, service_metadata: ServiceMetadata):
        logging.info(f"Running step ${self._name}")
        self._task.execute(service_metadata)
