# from abc import ABC, abstractmethod
from src.ec import *
from src.ec.util import *
from functools import cmp_to_key
import random

class Breeder:
    """
    A Breeder is a singleton object responsible for the breeding process during
    an evolutionary run. Only one Breeder is created and stored in the EvolutionState object.

    Breeders typically operate by applying a Species' breeding pipelines on
    subpopulations to produce new individuals.

    Breeders may be multithreaded, and care must be taken when accessing shared resources.
    """

    P_ELITE = "elite"
    P_REEVALUATE_ELITES = "reevaluate-elites"

    def __init__(self):
        self.elitenum = None
        self.toReevaluateElite = None
        self.operators = None
        self.operatorRate = None

    def setup(self, state:EvolutionState, base:Parameter):
        p = Parameter(state.P_POP).push(Population.P_SIZE)

        size = state.parameters.getInt(p, None)

        self.elitenum = [int]*size
        self.toReevaluateElite = [bool]*size

        for x in range(size):
            if state.parameters.exists(base.push(self.P_ELITE).push(""+str(x))):
                self.elitenum[x] = state.parameters.getInt(base.push(self.P_ELITE).push(""+str(x)),None)
            else:
                self.elitenum[x] = 1
            
            if state.parameters.exists(base.push(self.P_REEVALUATE_ELITES).push(""+str(x))):
                self.toReevaluateElite[x] = state.parameters.getBoolean(base.push(self.P_REEVALUATE_ELITES).push(""+str(x)),True)
            else:
                self.toReevaluateElite[x] = True

    def breedPopulation(self, state:EvolutionState)->Population:
        """
        Breeds state.population, returning a new population. In general,
        state.population should not be modified.
        """
        newpop = state.population.emptyclone()

        self.loadElites(state, newpop)

        '''
        1. parallely use one of the operator to produce new individuals
        '''

        op = random.choices(self.operators, weights=self.operatorRate, k=1)[0]

        # use subpopulation.duplicateSet to eliminate duplicate individuals
        '''
        2. local search
        '''
        pass

    def loadElites(self, state:EvolutionState, newpop:Population):
        for x in range(len (state.population.subpops) ):
            if self.elitenum[x] >= len( state.population.subpops[x].individuals ):
                state.output.error("The number of elites for subpopulation " + str(x) 
                                   + " equals or exceeds the actual size of the subpopulation")
                
        for x in range(len(state.population.subpops)):
            if self.elitenum[x] == 1: #  if the number of elites is 1, then we handle this by just finding the best one.
                bestInd = None
                for ind in state.population.subpops[x].individuals:
                    if bestInd is None or ind.fitness.betterThan(bestInd.fitness):
                        bestInd = ind
                    
                inds = newpop.subpops[x].individuals
                inds[len(inds) - 1] = bestInd.clone()
            elif self.elitenum[x] > 1: # we will need to sort
                sortedInds = sorted(state.population.subpops[x].individuals, key=cmp_to_key(compare))

                inds = newpop.subpops[x].individuals
                
                for x in range(len(inds) - self.elitenum[x], len(inds)):
                    inds[x] = sortedInds[x].clone()

        # optionally force reevaluation
        for x in range(len(state.population.subpops)):
            if self.toReevaluateElite[x] == True:
                for e in range(self.elitenum[x]):
                    length = len( newpop.subpops[x].individuals )
                    newpop.subpops[x].individuals[length - e - 1].evaluated = False
                
                 

def compare(a:GPIndividual, b:GPIndividual):
    if a.fitness.betterThan(b.fitness):
        return 1
    elif b.fitness.betterThan(a.fitness):
        return -1
    return 0