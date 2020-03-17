
from abc import ABC
from abc import abstractmethod


class AbstractTask:
    
    @abstractmethod
    def execute(self):
        ...
