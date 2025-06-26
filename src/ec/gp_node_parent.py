from abc import ABC, abstractmethod
from copy import __deepcopy__

class GPNodeParent(ABC):
    def __init__(self):
        pass

    def __deepcopy__(self):
        self.clone()