


class GPBuilder:

    P_MAXDEPTH = "max-depth"
    P_MINDEPTH = "min-depth"
    P_PROBCON = "prob_constant"

    def __init__(self):
        self.maxDepth:int = 3
        self.minDepth:int = 1
        self.probCons = 0.5

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

        self.probCons = state.parameters.getDoubleWithDefault(base.push(self.P_PROBCON), def_base.push(self.P_PROBCON))
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
        terminals = func_set.terminals[t]
        nonterminals = func_set.nonterminals[t]
        nodes = func_set.nodes[t]

        if len(nodes) == 0:
            self.output.error("there is no node for a certain type")

        if ((current + 1 >= max_depth or self.warn_about_nonterminal(len(nonterminals) == 0, type_, False, state))
            and (tried_terminals := True)
            and len(terminals) != 0):

            n = terminals[state.random[thread].randint(0, len(terminals) - 1)].light_clone()
            n.reset_node(state, thread)
            n.argposition = argposition
            n.parent = parent
            return n
        else:
            if tried_terminals:
                self.warn_about_no_terminal_with_type(type_, False, state)

            nodes_to_pick = func_set.nonterminals[t]
            if not nodes_to_pick:
                nodes_to_pick = func_set.terminals[t]

            n = nodes_to_pick[state.random[thread].randint(0, len(nodes_to_pick) - 1)].light_clone()
            n.reset_node(state, thread)
            n.argposition = argposition
            n.parent = parent

            childtypes = n.constraints(state.initializer).childtypes
            n.children = [self.full_node(state, current + 1, max_depth, ct, thread, n, i, func_set) for i, ct in enumerate(childtypes)]
            return n

    def full_node(self, state:EvolutionState, current:int, max_depth:int, thread:int, 
    parent:GPNodeParent, argposition:int, func_set:GPPrimitiveSet):
        tried_terminals = False

        t = type_.type
        terminals = func_set.terminals[t]
        nodes = func_set.nodes[t]

        if len(nodes) == 0:
            self.error_about_no_node_with_type(type_, state)

        if ((current + 1 >= max_depth)
            and (tried_terminals := True)
            and len(terminals) != 0):

            n = terminals[state.random[thread].randint(0, len(terminals) - 1)].light_clone()
            n.reset_node(state, thread)
            n.argposition = argposition
            n.parent = parent
            return n
        else:
            if tried_terminals:
                self.warn_about_no_terminal_with_type(type_, False, state)

            n = nodes[state.random[thread].randint(0, len(nodes) - 1)].light_clone()
            n.reset_node(state, thread)
            n.argposition = argposition
            n.parent = parent

            childtypes = n.constraints(state.initializer).childtypes
            n.children = [self.grow_node(state, current + 1, max_depth, ct, thread, n, i, func_set) for i, ct in enumerate(childtypes)]
            return n