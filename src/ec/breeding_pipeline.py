from abc import ABC, abstractmethod
from typing import List

from src.ec.util.parameter import Parameter
from src.ec.population import Population
from src.ec.evolution_state import EvolutionState
from src.ec.gp_individual import GPIndividual
from src.ec.breeding_source import BreedingSource
from src.ec.selection_method import SelectionMethod

import random

class BreedingPipeline(ABC, BreedingSource):
    '''
    BreedingPipeline is a concrete subclass of BreedingSource that performs genetic operations like crossover, mutation, or reproduction. 
    It takes input from one or more other BreedingSources (often SelectionMethods), applies a genetic operator, and outputs individuals.
    '''
    '''Here, I directly implement the MultiBreedingPipeline in ECJ'''
    #Indicates that a source is the exact same source as the previous source.
    V_SAME = "same" 

    #Indicates the probability that the Breeding Pipeline will perform its mutative action instead of just doing reproduction.
    P_LIKELIHOOD = "likelihood"

    # Indicates that the number of sources is variable and determined by the user in the parameter file.
    DYNAMIC_SOURCES = -1

    #Standard parameter for number of sources (only used if numSources returns DYNAMIC_SOURCES
    P_NUMSOURCES = "num-sources"

    #Standard parameter for individual-selectors associated with a BreedingPipeline
    P_SOURCE = "source"

    P_MULTIBREED = "multibreed"

    def __init__(self):
        self.mybase:Parameter = None
        self.likelihood = 1.0
        self.sources: List[BreedingSource] = []
        self.operatorRate: List[float] = []

    @abstractmethod
    def numSources(self):
        return len(self.sources)

    def minChildProduction(self):
        if len(self.sources) == 0:
            return 0
        return min(s.typicalIndsProduced() for s in self.sources)

    def maxChildProduction(self):
        if len(self.sources) == 0:
            return 0
        return max(s.typicalIndsProduced() for s in self.sources)

    def typicalIndsProduced(self):
        return self.maxChildProduction()

    def setup(self, state:EvolutionState, base:Parameter):
        super().setup(state, base)
        self.mybase = base
        def_:Parameter = self.defaultBase()

        self.likelihood = state.parameters.getDoubleWithDefault(
            base.push(self.P_LIKELIHOOD), def_.push(self.P_LIKELIHOOD), 1.0
        )
        if self.likelihood < 0.0 or self.likelihood > 1.0:
            state.output.fatal(f"Breeding Pipeline likelihood must be between 0.0 and 1.0 inclusive for"
                               +f"{base.push(self.P_LIKELIHOOD)} or {def_.push(self.P_LIKELIHOOD)}")

        numsources:int = self.numSources()
        if numsources == self.DYNAMIC_SOURCES:
            numsources = state.parameters.getInt(base.push(self.P_NUMSOURCES), def_.push(self.P_NUMSOURCES), 0)
            if numsources == -1:
                state.output.fatal("Breeding pipeline num-sources must exist and be >= 0",
                                   base.push(self.P_NUMSOURCES), def_.push(self.P_NUMSOURCES))
        elif numsources <= self.DYNAMIC_SOURCES:
            raise RuntimeError("numSources() returned < DYNAMIC_SOURCES")
        elif state.parameters.exists(base.push(self.P_NUMSOURCES), def_.push(self.P_NUMSOURCES)):
            state.output.warning("Breeding pipeline's number of sources is hard-coded to " + str(numsources) +
                                 " yet num-sources was provided: num-sources will be ignored.",
                                 base.push(self.P_NUMSOURCES), def_.push(self.P_NUMSOURCES))

        self.sources = [None] * numsources
        for x in range(numsources):
            p = base.push(self.P_SOURCE).push(str(x))
            d = def_.push(self.P_SOURCE).push(str(x))
            s = state.parameters.getString(p, d)
            if s is not None and s == self.V_SAME:
                if x == 0:
                    state.output.fatal("Source #0 cannot be declared with \"same\".", p, d)
                self.sources[x] = self.sources[x - 1]
            else:
                self.sources[x] = state.parameters.getInstanceForParameter(p, d, BreedingSource)
                self.sources[x].setup(state, p)
                self.operatorRate[x] = state.parameters.getDoubleWithDefault(p.push(self.P_PROB), d.push(self.P_PROB))


    def clone(self):
        # import copy
        # c = copy.copy(self)
        c = super().clone()
        c.sources = [None] * len( self.sources )
        c.operatorRate = [None] * len(self.operatorRate)
        c.likelihood = self.likelihood
        for x in range(len(self.sources)):
            if x == 0 or self.sources[x] != self.sources[x - 1]:
                c.sources.append(self.sources[x].clone())
                c.operatorRate.append(self.operatorRate[x])
            else:
                c.sources.append(c.sources[x - 1])
                c.operatorRate.append(c.operatorRate[x - 1])
        return c

    def reproduce(self, 
                  n:int, 
                  start:int, 
                  subpopulation:int, 
                  inds:List[GPIndividual], 
                  state:EvolutionState, 
                  thread:int, 
                  produceChildrenFromSource:bool)->int:
        if produceChildrenFromSource:
            self.sources[0].produce(n, n, start, subpopulation, inds, state, thread)
        if isinstance(self.sources[0], SelectionMethod):
            for q in range(start, n + start):
                inds[q] = inds[q].clone()
        return n

    def produces(self, 
                 state:EvolutionState, 
                 newpop:Population, 
                 subpopulation:int, 
                 thread:int) -> bool:
        for x in range(len(self.sources)):
            if x == 0 or self.sources[x] != self.sources[x - 1]:
                if not self.sources[x].produces(state, newpop, subpopulation, thread):
                    return False
        return True

    def prepareToProduce(self, 
                         state:EvolutionState, 
                         subpopulation:int, 
                         thread:int):
        for x in range(len(self.sources)):
            if x == 0 or self.sources[x] != self.sources[x - 1]:
                self.sources[x].prepareToProduce(state, subpopulation, thread)

    def finishProducing(self, 
                         state:EvolutionState, 
                         subpopulation:int, 
                         thread:int):
        for x in range(len(self.sources)):
            if x == 0 or self.sources[x] != self.sources[x - 1]:
                self.sources[x].finishProducing(state, subpopulation, thread)

    # def preparePipeline(self, hook):
    #     for source in self.sources:
    #         source.preparePipeline(hook)

    # def individualReplaced(self, 
    #                        state:EvolutionState, 
    #                        subpopulation:int, 
    #                        thread:int, 
    #                        individual:int):
    #     for source in self.sources:
    #         # if isinstance(source, SteadyStateBSourceForm):
    #         #     source.individualReplaced(state, subpopulation, thread, individual)
    #         pass

    # def sourcesAreProperForm(self, 
    #                          state:EvolutionState):
    #     for x, source in enumerate(self.sources):
    #         # if not isinstance(source, SteadyStateBSourceForm):
    #         #     state.output.error("Source is not SteadyStateBSourceForm",
    #         #                        self.mybase.push(self.P_SOURCE).push(str(x)),
    #         #                        self.defaultBase().push(self.P_SOURCE).push(str(x)))
    #         # else:
    #         #     source.sourcesAreProperForm(state)
    #         pass

    def defaultBase(self)->Parameter:
        # Placeholder: override as needed
        return self.mybase.push(self.P_MULTIBREED)
    
    def produce(self, min:int, max:int, start:int, subpopulation:int, inds:list[GPIndividual], 
                state:EvolutionState, thread:int)->int:
        op = random.choices(self.sources, weights=self.operatorRate, k=1)[0]

        total = op.produce(min,max,start,subpopulation,inds,state,thread)

        if isinstance(op, SelectionMethod):
            for q in range(start, total+start):
                inds[q] = inds[q].clone()
        
        return total