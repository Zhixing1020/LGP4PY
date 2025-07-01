from src.ec import *
from src.ec.util import *
from typing import List
import random

class MultiBreedingPipeline(BreedingPipeline):
    '''Here, I directly implement the MultiBreedingPipeline in ECJ'''

    P_MULTIBREED = "multibreed"

    def __init__(self):
        super().__init__()

    def numSources(self):
        return len(self.sources)
    
    def setup(self, state:EvolutionState, base:Parameter):
        super().setup(state, base)

        # def_p = self.defaultBase()

    def defaultBase(self)->Parameter:
        # Placeholder: override as needed
        return self.mybase.push(self.P_MULTIBREED)
    
    def produce(self, min:int, max:int, start:int, subpopulation:int, inds:list[GPIndividual], 
                state:EvolutionState, thread:int)->tuple[int, list[GPIndividual]]:
        op = random.choices(self.sources, weights=self.operatorRate, k=1)[0]

        total, res = op.produce(min,max,start,subpopulation,inds,state,thread)

        if isinstance(op, SelectionMethod):
            for q in range(start, total+start):
                inds[q] = inds[q].clone()

        # res = [ind for ind in inds[start:start+total]]

        # recording the major operator that produces this new individual
        for q in res:
            q.breedingPipe = op
        
        return total, res