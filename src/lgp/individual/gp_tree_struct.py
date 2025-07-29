from src.ec.gp_tree import GPTree
from src.ec.gp_node import GPNode
from src.ec.evolution_state import EvolutionState
from tasks.problem import Problem

from typing import Set, List
# from copy import deepcopy

class GPTreeStruct(GPTree):
    ARITHMETIC = 0
    BRANCHING = 1
    ITERATION = 2

    def __init__(self):
        super().__init__()
        self.status: bool = False  # False: non-effective, True: effective
        self.effRegisters: Set[int] = set()
        self.type: int = GPTreeStruct.ARITHMETIC  # default: ARITHMETIC

    def __repr__(self):
        address = hex(id(self))
        return f"{str(self)}<GPTreeStruct {address} status={self.status}>"


    def updateEffRegister(self, s: Set[int]):
        self.child.collectReadRegister(s)

    def collectReadRegister(self) -> Set[int]:
        s = set()
        self.child.collectReadRegister(s)
        return s

    # def collectReadRegister_list(self) -> List[int]:
    #     l = []
    #     self.child.collectReadRegister_list(l)
    #     return l

    def clone(self) -> 'GPTreeStruct':
        t = self.lightClone()
        t.child = self.child.clone()
        t.child.parent = t
        t.child.argposition = 0
        t.status = self.status
        t.effRegisters = set(self.effRegisters)
        t.type = self.type
        return t

    def lightClone(self) -> 'GPTreeStruct':
        t = super().lightClone()
        return t

    def assignfrom(self, tree: 'GPTree'):
        self.child = tree.child
        self.owner = tree.owner
