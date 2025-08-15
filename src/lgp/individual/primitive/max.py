from src.ec import *
from tasks.problem import Problem
from typing import override

# from src.ec.gp_node import GPNode
# from src.ec.gp_data import GPData

class Max(GPNode):
    
    def __str__(self):
        return "max"
    
    @override
    def expectedChildren(self)->int:
        return 2
    
    @override
    def eval(self, state: EvolutionState, thread: int, input: GPData,
             individual, problem: Problem):
        child_result = input
        
        self.children[0].eval(state, thread, child_result, individual, problem)
        result = child_result.value

        self.children[1].eval(state, thread, child_result, individual, problem)
        child_result.value = max(result, child_result.value)

        # input.value = child_result.value