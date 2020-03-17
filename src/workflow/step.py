import logging
from tasks.abstract_task import AbstractTask


class Step:

    def __init__(self, name: str, task: AbstractTask):
        self._name = name
        self._task = task

    def run(self):
        logging.info(f"Running step ${self._name}")
        self._task.execute()
