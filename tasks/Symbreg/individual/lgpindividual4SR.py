from src.lgp.individual.lgp_individual import LGPIndividual

class LGPIndividual4SR(LGPIndividual):

    def __init__(self, state=None, base=None, def_base=None):
        super().__init__(state, base, def_base)

    def execute(state, thread, input, individual, problem):
        return super().execute(thread, input, individual, problem)
    
    def preExecution(state, thread):
        return super().preExecution(thread)
    
    def postExecution(state, thread):
        return super().postExecution(thread)
    
    def makeGraphvizRule(self):
        return super().makeGraphvizRule()