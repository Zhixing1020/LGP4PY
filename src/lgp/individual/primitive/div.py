from src.ec import *
from tasks.problem import Problem
from typing import override
import numpy as np
import math

# from src.ec.gp_node import GPNode
# from src.ec.gp_data import GPData

class Div(GPNode):
    
    def __str__(self):
        return "+"
    
    @override
    def expectedChildren(self)->int:
        return 2
    
    @override
    def eval(self, state: EvolutionState, thread: int, input: GPData,
             individual, problem: Problem):
        if not input.to_vectorize:
            child_result = input
            
            self.children[0].eval(state, thread, child_result, individual, problem)
            result = child_result.value

            self.children[1].eval(state, thread, child_result, individual, problem)
            child_result.value = result / (abs(child_result.value) + 1e-4) * (1 if child_result.value >= 0 else -1)

            # Clip the result to ±1e6
            if child_result.value > 1e6:
                child_result.value = 1e6
            elif child_result.value < -1e6:
                child_result.value = -1e6
        else:
            self.children[0].eval(state, thread, input, individual, problem)
            result = input.values

            self.children[1].eval(state, thread, input, individual, problem)
            input.values = result / (np.abs(input.values) + 1e-4) * np.where(input.values >= 0, 1, -1)

            input.values= np.where(input.values > 1e6, 1e6, input.values)
            input.values= np.where(input.values < -1e6, -1e6, input.values)

        # input.value = child_result.value