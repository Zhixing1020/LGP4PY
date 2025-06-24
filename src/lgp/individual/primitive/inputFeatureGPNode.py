from src.ec import *
from tasks import Problem
from typing import override

from src.ec.GPNode import GPNode

class InputFeatureGPNode(GPNode):
    
    def __init__(self, index:int=0, range:int=1):
        super().__init__()
        self.index = index
        self.range = range

        if index >= range or index < 0:
            raise SystemExit("Fatal error: illegal index of InputFeatureGPNode\n")

    def get_index(self):
        return self.index

    def get_range(self):
        return self.range

    def set_index(self, ind):
        self.index = ind

    def set_range(self, size):
        self.range = size

    def __str__(self):
        return f"In{self.index}"

    @override
    def expectedChildren(self):
        return 0
    
    @override
    def eval(self, state: EvolutionState, thread: int, input: GPData,
             individual, problem: Problem):
        if hasattr(problem, 'datadim') and self.range != problem.datadim and state is not None:
            self.set_range(problem.datadim)
            self.index = state.random[thread].randint(0, self.range - 1)

        if self.index < len(problem.X):
            input.value = problem.X[self.index]
        else:
            print("The input index exceeds the data dimension")
            exit(1)

    @override
    def nodeEquivalentTo(self, other: GPNode) -> bool:
        return isinstance(other, InputFeatureGPNode) and self.index == other.index
    
    @override
    def resetNode(self, state:EvolutionState, thread:int):
        self.index = state.random[thread].randint(0, self.range - 1)

    @override
    def lightClone(self):
        clone = super().lightClone()
        clone.set_index(self.index)
        clone.set_range(self.range)
        return clone