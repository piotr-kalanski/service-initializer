from typing import List
from workflow.step import Step


class WorkflowConfiguration:
    
    def __init__(self):
        self._steps = []

    def add_step(self, step: Step):
        self._steps.append(step)

    def get_steps(self) -> List[Step]:
        return self._steps
