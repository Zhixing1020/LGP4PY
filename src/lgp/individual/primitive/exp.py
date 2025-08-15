from src.ec import * 
import math
from tasks.problem import Problem
from typing import override

class Exp(GPNode):

    @override
    def expectedChildren(self):
        return 1

    @override
    def eval(self, state: EvolutionState, thread: int, input: GPData,
             individual, problem: Problem):
        child_result = input
        
        self.children[0].eval(state, thread, child_result, individual, problem)
        result = child_result.value
        if child_result.value > 10:
            result = 10
        
        input.value = math.exp(result)
        if input.value > 1e6:
            input.value = 1e6

    def __str__(self):
        return "exp"