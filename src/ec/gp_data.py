from dataclasses import dataclass
# from copy import deepcopy

@dataclass
class GPData:
    value:float = 0.0

    # def __deepcopy__(self):
    #     d = self.__class__
    #     d.value = self.value

    # def __init__(self):
    #     self.value = 0.0

    # def clone(self):
    #     d = self.__class__
    #     d.value = self.value