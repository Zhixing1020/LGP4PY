from src.ec import *
from tasks import Problem
from typing import override

# from src.ec.gp_node import GPNode

class InputFeatureGPNode(GPNode):
    
    def __init__(self, index:int=0, range:int=1):
        super().__init__()
        self.index = index
        self.range = range

        if index >= range or index < 0:
            raise SystemExit("Fatal error: illegal index of InputFeatureGPNode\n")

    def getIndex(self):
        return self.index

    def getRange(self):
        return self.range

    def setIndex(self, ind):
        self.index = ind

    def setRange(self, size):
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
            self.setRange(problem.datadim)
            self.index = state.random[thread].randint(0, self.range - 1)

        if self.index < len(problem.X):
            input.value = problem.X[self.index]
        else:
            print("The input index exceeds the data dimension")
            exit(1)

    def __eq__(self, other):
        res = super().__eq__(other)
        return res and self.index == other.getIndex()
    
    @override
    def resetNode(self, state:EvolutionState, thread:int):
        self.index = state.random[thread].randint(0, self.range - 1)

    @override
    def lightClone(self):
        clone = super().lightClone()
        clone.setIndex(self.index)
        clone.setRange(self.range)
        return clone