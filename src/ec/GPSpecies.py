from ec.util import *
from ec import *
from abc import ABC, abstractmethod
from typing import Type

class GPSpecies(ABC):
    P_INDIVIDUAL: str = "ind"
    P_PIPE: str = "pipe"
    P_FITNESS: str = "fitness"

    def __init__(self):
        self.i_prototype: GPIndividual = None
        self.pipe_prototype: BreedingPipeline = None
        self.f_prototype: Fitness = None

    def clone(self):
        new_species = self.__class__()
        new_species.i_prototype = self.i_prototype.clone()
        new_species.f_prototype = self.f_prototype.clone()
        new_species.pipe_prototype = self.pipe_prototype.clone()
        return new_species

    def new_individual(self, state: EvolutionState, thread: int) -> GPIndividual:
        newind = self.i_prototype.clone()

        # Initialize the trees
        for tree in newind.trees:
            tree.build_tree(state, thread)

        newind.fitness = self.f_prototype.clone()
        newind.evaluated = False
        newind.species = self
        return newind

    def setup(self, state: EvolutionState, base: Parameter):
        default = self.default_base()

        self.pipe_prototype = state.parameters.get_instance_for_parameter(
            base.push(self.P_PIPE), default.push(self.P_PIPE), BreedingPipeline)
        self.pipe_prototype.setup(state, base.push(self.P_PIPE))
        state.output.exit_if_errors()

        self.i_prototype = state.parameters.get_instance_for_parameter(
            base.push(self.P_INDIVIDUAL), default.push(self.P_INDIVIDUAL), GPIndividual)
        self.i_prototype.species = self
        self.i_prototype.setup(state, base.push(self.P_INDIVIDUAL))
        # Ensure individual prototype is a GPIndividual
        if not isinstance(self.i_prototype, GPIndividual):
            state.output.fatal(f"The Individual class for the Species {self.__class__.__name__} must be a subclass of GPIndividual.", base)

        self.f_prototype = state.parameters.get_instance_for_parameter(
            base.push(self.P_FITNESS), default.push(self.P_FITNESS), Fitness)
        self.f_prototype.setup(state, base.push(self.P_FITNESS))

    @abstractmethod
    def default_base(self) -> Parameter:
        return GPDefaults.base().push(self.P_GPSPECIES)