from typing import List

from ec import *
from ec.util import *

class Fitness:

    P_MAXIMIZE = "maximize"

    def __init__(self):

        self.maximize: bool = False
        self.value: float = 1e7

    def clone(self):
        new_fitness = Fitness()
        new_fitness.value = self.value
        new_fitness.maximize = self.maximize
        return new_fitness

    def setup(self, state:EvolutionState, base:Parameter):
        
        def_param = self.default_base()
       
        self.maximize = state.parameters.getBoolean(base.push(self.P_MAXIMIZE), def_param.push(self.P_MAXIMIZE), False)

        # for i in range(num):
        #     self.min_objective[i] = state.parameters.get_double_with_default(base.push(self.P_MINOBJECTIVES).push(str(i)), def_param.push(self.P_MINOBJECTIVES).push(str(i)), 0.0)
        #     self.max_objective[i] = state.parameters.get_double_with_default(base.push(self.P_MAXOBJECTIVES).push(str(i)), def_param.push(self.P_MAXOBJECTIVES).push(str(i)), 1.0)
        #     self.maximize[i] = state.parameters.get_boolean(base.push(self.P_MAXIMIZE).push(str(i)), def_param.push(self.P_MAXIMIZE).push(str(i)), True)

        #     if self.min_objective[i] >= self.max_objective[i]:
        #         state.output.error(f"For objective {i} the min fitness must be strictly less than the max fitness.")

        # state.output.exit_if_errors()

    def setFitness(self, state:EvolutionState, fit:float):
        self.value = float
    
    def fitness(self)->float:
        return self.value

    def is_ideal_fitness(self):
        return False

    def equivalent_to(self, other:Fitness)->bool:
        if not isinstance(other, Fitness):
            return False

        if self.maximize != other.maximize:
            raise RuntimeError("Mismatched optimization directions")

        if self.value == other.value:
            return True
        else:
            return False

    def better_than(self, other)->bool:
        if self.maximize:
            return True if self.value > other.value else False
        else:
            return True if self.value < other.value else False


    def default_base(self):
        return GPDefaults.base().push(self.P_FITNESS)
    
    def __str__(self):
        return self.value

    def read_fitness(self, state, reader):
        line = reader.readline()
        self.value = float(line)

        # if not line.startswith(self.FITNESS_PREAMBLE + self.MULTI_FITNESS_POSTAMBLE):
        #     state.output.fatal(f"Invalid fitness preamble: {line}")
        # line = line[len(self.FITNESS_PREAMBLE + self.MULTI_FITNESS_POSTAMBLE):].strip("\n ")
        # tokens = line.rstrip(self.FITNESS_POSTAMBLE).split()
        # if len(tokens) != len(self.objectives):
        #     state.output.fatal(f"Expected {len(self.objectives)} fitness values, got {len(tokens)}")
        # self.objectives = [float(tok) for tok in tokens]
