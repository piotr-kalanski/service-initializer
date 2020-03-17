from tasks.abstract_task import AbstractTask


class Step:

    def __init__(self, name: str, task: AbstractTask):
        self._name = name
        self._task = task
