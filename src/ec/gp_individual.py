from src.ec.gp_tree import GPTree
from src.ec.gp_defaults import GPDefaults
# from src.ec.gp_individual import GPIndividual
from src.ec.gp_node import GPNode
from copy import __deepcopy__

class GPIndividual:
    '''A simple GP individual with only one tree'''
    P_NUMTREES = "numtrees"
    P_TREE = "tree"
    P_INDIVIDUAL = "individual"
    EVALUATED_PREAMBLE = "Evaluated: "

    def __init__(self):
        self.treelist:[GPTree] = []*1
        self.evaluated = False
        self.fitness = None
        self.species = None

    @classmethod
    def default_base(cls):
        return GPDefaults.base().push(cls.P_INDIVIDUAL)

    def __eq__(self, other):
        return self.equals(other)
        
    def equals(self, ind:'GPIndividual'):
        if ind is None:
            return False
        if not isinstance(ind, GPIndividual):
            return False
        if len(self.treelist) != len(ind.treelist):
            return False
        return all(self_tree.treeEquals(other_tree) for self_tree, other_tree in zip(self.treelist, ind.treelist))
    
    def setup(self, state, base):

        def_base = self.default_base()
        self.evaluated = False

        # t = state.parameters.getInt(base.push(self.P_NUMTREES), def_base.push(self.P_NUMTREES), 1)
        # if t <= 0:
        #     state.output.fatal("A GPIndividual must have at least one tree.", base.push(self.P_NUMTREES), def_base.push(self.P_NUMTREES))

        # self.trees = [None] * t
        # for x in range(t):
        #     p = base.push(self.P_TREE).push(str(x))
        #     self.trees[x] = state.parameters.getInstanceForParameterEq(p, def_base.push(self.P_TREE).push(str(x)), GPTree)
        #     self.trees[x].owner = self
        #     self.trees[x].setup(state, p)
        self.treelist = [GPTree]*1
        p = base.push(self.P_TREE).push(str(0))
        self.trees[0] = state.parameters.getInstanceForParameterEq(p, def_base.push(self.P_TREE).push(str(0)), GPTree)
        self.trees[0].owner = self
        self.trees[0].setup(state, p)

        initializer = state.initializer  # expected to be GPInitializer
        for x in range(t):
            constraints = self.trees[x].constraints(initializer)
            for node_array in constraints.functionset.nodes:
                for node in node_array:
                    node.check_constraints(state, x, self, base)

    def printTrees(self)->str:
        res = ""
        for tree, i in self.treelist, range(len(self.treelist)):
            res += f"Tree {i}: {tree}"

        return res
    
    def printIndividualForHuman(self)->str:
        res = ""
        res += self.EVALUATED_PREAMBLE + ("true" if self.evaluated else "false") + "\n"
        res += "Fitness: " + self.fitness + "\n"
        
        res += self.printTrees() + "\n"

        return res
    
    def clone(self):
        myobj = self.__class__()
        myobj.fitness = self.fitness.clone() if self.fitness is not None else None
        myobj.treelist = [tree.clone() for tree in self.treelist]
        for tree in myobj.trees:
            tree.owner = myobj
        myobj.evaluated = self.evaluated
        return myobj

    def lightClone(self):
        myobj = self.__class__()
        myobj.fitness = self.fitness.clone() if self.fitness is not None else None
        myobj.treelist = [tree.lightClone() for tree in self.treelist]
        for tree in myobj.trees:
            tree.owner = myobj
        myobj.evaluated = self.evaluated
        return myobj
    
    def __deepcopy__(self):
        self.clone()

    def size(self):
        return sum(tree.child.num_nodes(GPNode.NODESEARCH_ALL) for tree in self.treelist)
    
    def getTree(self, index:int)->GPTree:
        return self.treelist[index]
    
    def getTrees(self)->[GPTree]:
        return self.treelist
    
    def setTree(self, index:int, tree:GPTree)->bool:
        if index < len(self.treelist):
            self.treelist[index] = tree
            return True
        else:
            print(f"setTree index: {index} is out of range " + len(self.treelist))
            return False
        
    def getTreesLength(self)->int:
        return len(self.treelist)
