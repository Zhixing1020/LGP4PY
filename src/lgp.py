"""The :mod:`lgp` module provides the necessary methods and classes to perform
Linear Genetic Programming (LGP) with DEAP. It provides necessary functions run LGP.
The behaviors of LGP is defined by a parameter file

This file is equivalent to "Evolve.java" in ECJ
"""

'''
Use the ideas of ECJ to use and reimplement the functions of DEAP.
'''


# import classes and files
import sys
sys.path.append('D:/zhixing/科研/LGP4PY/LGP4PY')
from src.ec import *
from src.ec.util import *

# set up LGP behaviors
'''read parameters from the parameter file and set it into pset and toolbox'''

# define main() and run main()  

if __name__ == "__main__":
    
    state = EvolutionState('D:\\zhixing\\科研\\LGP4PY\\LGP4PY\\tasks\\Symbreg\\parameters\\LGP_test.params')
    state.setup("")

    # builder = GPBuilder()
    # builder.setup(state, Parameter("gp.koza.half"))
    # state.primitive_set = GPPrimitiveSet()
    # state.primitive_set.setup(state, Parameter('gp.fs.0'))  # here, I need to use a default parameter name
    # # fun_set = {Add(), InputFeatureGPNode()}
    
    # tree = GPTree()
    # for _ in range(0,10):
    #     tree.child = builder.newRootedTree(state, 0, tree, state.primitive_set, 0)
    #     print(str(tree) + "\t\t" + str(tree.child.numNodes(GPNode.NODESEARCH_ALL)) + "\t\t" + str(tree.child.numNodes(GPNode.NODESEARCH_NONTERMINALS)))
    
    # individual = GPIndividual()
    # individual.setup(state, Parameter('pop.subpop.0.species.ind'))
    # individual.getTree(0).child = builder.newRootedTree(state, 0, individual.getTree(0), state.primitive_set, 0)
    # individual.fitness = Fitness()

    # print( individual.printIndividualForHuman() )

    # species = GPSpecies()
    # species.setup(state, Parameter('pop.subpop.0.species'))

    # subpop = Subpopulation()
    # subpop.setup(state, Parameter('pop.subpop.0'))
    # subpop.populate(state, 0)

    pop = Population()
    pop.setup(state, Parameter('pop'))
    pop.populate(state, 0)

    # for tree in subpop.individuals:
    #     print(tree)
    print("stop")