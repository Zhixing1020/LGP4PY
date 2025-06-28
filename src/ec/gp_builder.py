# import sys
# sys.path.append('D:/zhixing/科研/LGP4PY/LGP4PY')

from src.ec.evolution_state import EvolutionState
from src.ec.gp_node import GPNode
from src.ec.gp_node_parent import GPNodeParent
from src.ec.gp_primitive_set import GPPrimitiveSet
from src.ec.gp_tree import GPTree
from src.ec.util.parameter import Parameter
from src.lgp.individual.primitive import *

class GPBuilder:

    P_MAXDEPTH = "max-depth"
    P_MINDEPTH = "min-depth"
    P_PROBCON = "prob_constant"
    P_BUILDER = "builder"

    def __init__(self):
        self.maxDepth:int = 3
        self.minDepth:int = 1
        self.probCons = 0.5

    @classmethod
    def default_base(cls)->Parameter:
        return Parameter(cls.P_BUILDER)

    def setup(self, state, base):
        # super().setup(state, base)
        def_base = self.default_base()

        self.maxDepth = state.parameters.getInt(base.push(self.P_MAXDEPTH), def_base.push(self.P_MAXDEPTH))
        if self.maxDepth <= 0:
            state.output.fatal("The Max Depth for a KozaBuilder must be at least 1.")

        self.minDepth = state.parameters.getInt(base.push(self.P_MINDEPTH), def_base.push(self.P_MINDEPTH))
        if self.minDepth <= 0:
            state.output.fatal("The Min Depth for a KozaBuilder must be at least 1.")

        if self.maxDepth < self.minDepth:
            state.output.fatal("Max Depth must be >= Min Depth for a KozaBuilder")

        self.probCons = state.parameters.getDoubleWithDefault(base.push(self.P_PROBCON), def_base.push(self.P_PROBCON), 0.5)
        if self.probCons < 0:
            state.output.fatal("The constant probability for a KozaBuilder must be >= 0.0")

    def can_add_constant(self, parent):
        root = parent
        if isinstance(root, FlowOperator):
            return True
        terminalsize = root.numNodes(GPNode.NODESEARCH_TERMINALS)
        constnatsize = root.numNodes(GPNode.NODESEARCH_CONSTANT)
        nullsize = root.numNodes(GPNode.NODESEARCH_NULL)
        if terminalsize > 0:
            return (constnatsize + 1) / (terminalsize + nullsize) <= self.probCons
        else:
            return False
        
    def full_node(self, state:EvolutionState, current:int, max_depth:int, thread:int, 
    parent:GPNodeParent, argposition:int, func_set:GPPrimitiveSet):
        tried_terminals = False

        # t = type_.type
        terminals = func_set.terminals
        nonterminals = func_set.nonterminals
        nodes = func_set.nodes

        if len(nonterminals) == 0:
            self.output.warning("there is NO nonterminals")

        if len(nodes) == 0:
            self.output.error("there is no node for a certain type")

        if ((current + 1 >= max_depth or len(nonterminals) == 0)
            and (tried_terminals := True)
            and len(terminals) != 0):

            n = state.random[thread].choice(terminals).lightClone()
            n.resetNode(state, thread)
            n.argposition = argposition
            n.parent = parent
            return n
        else:
            if tried_terminals:
                self.output.error("there is NO terminals")

            nodes_to_pick = func_set.nonterminals
            if nodes_to_pick is None or len(nodes_to_pick) == 0:
                nodes_to_pick = func_set.terminals

            n = state.random[thread].choice(nodes_to_pick).lightClone()
            n.resetNode(state, thread)
            n.argposition = argposition
            n.parent = parent

            n.children = [self.full_node(state, current + 1, max_depth, thread, n, i, func_set) for i, _ in enumerate(n.children)]

            return n
    
    def newRootedTree(self, state:EvolutionState, thread:int, parent:GPNodeParent, set:GPPrimitiveSet, argposition:int)->GPNode:
        return self.full_node(state, 0, state.random[thread].randint(0, self.maxDepth-self.minDepth) + self.minDepth,
                         thread,parent,argposition,set)
    

if __name__ == "__main__":
    
    from src.ec.util.parameter import Parameter
    builder = GPBuilder()
    
    state = EvolutionState('D:\\zhixing\\科研\\LGP4PY\\LGP4PY\\tasks\\Symbreg\\parameters\\LGP_test.params')
    state.setup("")
    builder.setup(state, Parameter("gp.koza.half"))
    state.primitive_set = GPPrimitiveSet()
    state.primitive_set.setup(state, Parameter('gp.fs.0'))  # here, I need to use a default parameter name
    # fun_set = {Add(), InputFeatureGPNode()}
    tree = GPTree()
    for _ in range(0,10):
        tree.child = builder.newRootedTree(state, 0, tree, state.primitive_set, 0)
        print(tree)
