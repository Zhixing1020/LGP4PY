from src.ec import * 
import math
from tasks.problem import Problem
from typing import override

class Ln(GPNode):

    @override
    def expectedChildren(self):
        return 1

    @override
    def eval(self, state: EvolutionState, thread: int, input: GPData,
             individual, problem: Problem):
        child_result = input
        
        self.children[0].eval(state, thread, child_result, individual, problem)
        result = child_result.value
        
        input.value = math.log( abs(result) + 1e-10)

    def __str__(self):
        return "ln"