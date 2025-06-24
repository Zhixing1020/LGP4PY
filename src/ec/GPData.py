
class GPData:

    def __init__(self):
        self.value = 0.0

    def clone(self):
        d = self.__class__
        d.value = self.value