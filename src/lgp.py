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
sys.path.append('D:/data/study/LGP4PY/LGP4PY')
from src.ec import *
from src.ec.util import *
# from tasks.Symbreg.optimization.gp_symbolic_regression import GPSymbolicRegression

# set up LGP behaviors
'''read parameters from the parameter file and set it into pset and toolbox'''

# define main() and run main()  



if __name__ == "__main__":
    Evolve.main()