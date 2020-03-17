from tasks.task import Task


class Step:

    def __init__(self, name: str, task: AbstractTask):
        self._name = name
        self._task = task
