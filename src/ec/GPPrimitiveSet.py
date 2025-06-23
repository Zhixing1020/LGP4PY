from typing import Set
from ec import *

class GPPrimitivesSet:

    P_NAME = "name"
    P_FUNC = "func"
    P_SIZE = "size"
    P_NUMREGISTERS = "numregisters"

    def __init__():
        self.nodes:Set[GPNode] = set()
        # self.nodes_by_name:Set[str] = set()

        self.nonterminals:Set[GPNode] = set()
        self.terminals:Set[GPNode] = set()

        self.registers:Set[GPNode] = set()
        self.nonregisters:Set[GPNode] = set()

        self.constants:Set[GPNode] = set()
        self.nonconstants:Set[GPNode] = set()

        self.flowoperators:Set[GPNode] = set()
        

    def setup(self, state:EvolutionState, base:Parameter):
        self.name = state.parameters.getString(base.push("name"), None)
        if self.name is None:
            state.output.fatal("No name was given for this function set.", base.push("name"))

        # old_fs = state.initializer.function_set_repository.get(self.name)
        # if old_fs is not None:
        #     state.output.fatal(f"The GPFunctionSet \"{self.name}\" has been defined multiple times.", base.push("name"))
        # state.initializer.function_set_repository[self.name] = self

        num_funcs = state.parameters.getInt(base.push("size"), None)
        if num_funcs < 1:
            state.output.error(f"The GPFunctionSet \"{self.name}\" has no function.")

        for x in range(num_funcs):
            pp = base.push("func").push(str(x))
            gpfi = state.parameters.getInstanceForParameter(pp, None, GPNode)
            gpfi.setup(state, pp)

            # Special handling
            if isinstance(gpfi, InputFeatureGPNode):
                rng = state.parameters.getInt(pp.push("size"), None, 0)
                gpfi.set_range(rng)

            elif isinstance(gpfi, ConstantGPNode):
                lb = state.parameters.getDouble(pp.push("lowbound"), None, 0.0)
                ub = state.parameters.getDouble(pp.push("upbound"), None, 1.0)
                step = state.parameters.getDouble(pp.push("step"), None, 0.1)
                if lb > ub:
                    state.output.fatal("the range of constants does not make sense")
                gpfi = ConstantGPNode(lb, ub, step)
                gpfi.setup(state, pp)

            elif isinstance(gpfi, FlowOperator):
                mbl1 = state.parameters.getInt(pp.push("maxbodylength"), None)
                if mbl1 < 1:
                    state.output.fatal("max body length must be >=1")
                mbl2 = state.parameters.getInt(pp.push("minbodylength"), None)
                if mbl2 < 1 or mbl2 > mbl1:
                    state.output.fatal(f"min body length is illegal, please check the setting of {pp.push('minbodylength')}")
                gpfi.set_max_body_length(mbl1)
                gpfi.set_min_body_length(mbl2)
            

            self.nodes.add(gpfi)
            # if str(gpfi) not in self.nodes_by_name:
            #     self.nodes_by_name.add(str(gpfi))
            # else:
            #     self.nodes_by_name[gpfi.name()].append(gpfi)

        for node in self.nodes:
            if node.expectedChildren() == 0:
                self.terminals.add(node)
                if isinstance(node, ReadRegisterGPNode):
                    self.registers.add(node)
                else:
                    self.nonregisters.add(node)
            else:
                self.nonterminals.add(node)

            if isinstance(node, InputFeatureGPNode) or isinstance(node, ConstantGPNode):
                self.constants.add(node)
            elif node.expectedChildren() == 0:
                self.nonconstants.add(node)

            if isinstance(node, FlowOperator):
                self.flowoperators.add(node)