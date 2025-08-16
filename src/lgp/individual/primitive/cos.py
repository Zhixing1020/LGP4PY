from src.ec import * 
import math
from tasks.problem import Problem
from typing import override
import numpy as np

class Cos(GPNode):
    @override
    def expectedChildren(self):
        return 1

    @override
    def eval(self, state: EvolutionState, thread: int, input: GPData,
             individual, problem: Problem):
        if not input.to_vectorize:
            child_result = input
            
            self.children[0].eval(state, thread, child_result, individual, problem)
            input.value = math.cos(child_result.value)
        else:
            self.children[0].eval(state, thread, input, individual, problem)
            input.values = np.cos(input.values)

    def __str__(self):
        return "cos"