from tasks.abstract_task import AbstractTask


class DummyTask(AbstractTask):
    
    def __init__(self):
        self.executed = False

    def execute(self):
        self.executed = True
