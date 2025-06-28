from abc import ABC, abstractmethod
from src.ec import *
from src.ec.util import *

class Breeder(ABC):
    """
    A Breeder is a singleton object responsible for the breeding process during
    an evolutionary run. Only one Breeder is created and stored in the EvolutionState object.

    Breeders typically operate by applying a Species' breeding pipelines on
    subpopulations to produce new individuals.

    Breeders may be multithreaded, and care must be taken when accessing shared resources.
    """

    # @abstractmethod
    def breedPopulation(self, state:EvolutionState)->Population:
        """
        Breeds state.population, returning a new population. In general,
        state.population should not be modified.
        """
        pass

    def setup(self, state:EvolutionState, base:Parameter):
        pass