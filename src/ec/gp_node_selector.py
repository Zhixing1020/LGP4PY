



class GPNodeSelector:
    P_NODESELECTOR = "ns"
    P_TERMINAL_PROBABILITY = "terminals"
    P_NONTERMINAL_PROBABILITY = "nonterminals"
    P_ROOT_PROBABILITY = "root"

    def __init__(self):
        self.rootProbability = 0.0
        self.terminalProbability = 0.0
        self.nonterminalProbability = 0.0
        self.nonterminals = -1
        self.terminals = -1
        self.nodes = -1
        self.reset()

    def default_base(self):
        return GPKozaDefaults.base().push(self.P_NODESELECTOR)

    def clone(self):
        s = KozaNodeSelector()
        s.rootProbability = self.rootProbability
        s.terminalProbability = self.terminalProbability
        s.nonterminalProbability = self.nonterminalProbability
        return s

    def setup(self, state, base):
        def_base = self.default_base()

        self.terminalProbability = state.parameters.get_double_with_max(
            base.push(self.P_TERMINAL_PROBABILITY),
            def_base.push(self.P_TERMINAL_PROBABILITY), 0.0, 1.0)
        if self.terminalProbability == -1.0:
            state.output.fatal("Invalid terminal probability for KozaNodeSelector")

        self.nonterminalProbability = state.parameters.get_double_with_max(
            base.push(self.P_NONTERMINAL_PROBABILITY),
            def_base.push(self.P_NONTERMINAL_PROBABILITY), 0.0, 1.0)
        if self.nonterminalProbability == -1.0:
            state.output.fatal("Invalid nonterminal probability for KozaNodeSelector")

        self.rootProbability = state.parameters.get_double_with_max(
            base.push(self.P_ROOT_PROBABILITY),
            def_base.push(self.P_ROOT_PROBABILITY), 0.0, 1.0)
        if self.rootProbability == -1.0:
            state.output.fatal("Invalid root probability for KozaNodeSelector")

        if self.rootProbability + self.terminalProbability + self.nonterminalProbability > 1.0:
            state.output.fatal("Probabilities for root, terminals, and nonterminals must not sum to more than 1.0")

        self.reset()

    def reset(self):
        self.nonterminals = self.terminals = self.nodes = -1

    def pickNode(self, state, subpopulation, thread, ind, tree, GPNodeType=None):
        if GPNodeType is not None:
            if self.nodes == -1:
                self.nodes = tree.child.numNodes(GPNodeType)
            if self.nodes > 0:
                return tree.child.nodeInPosition(state.random[thread].randint(0, self.nodes), GPNodeType)
            else:
                return tree.child

        rnd = state.random[thread].random()
        if rnd > self.nonterminalProbability + self.terminalProbability + self.rootProbability:
            if self.nodes == -1:
                self.nodes = tree.child.numNodes(GPNode.NODESEARCH_ALL)
            return tree.child.nodeInPosition(state.random[thread].randint(0, self.nodes), GPNode.NODESEARCH_ALL)
        elif rnd > self.nonterminalProbability + self.terminalProbability:
            return tree.child
        elif rnd > self.nonterminalProbability:
            if self.terminals == -1:
                self.terminals = tree.child.numNodes(GPNode.NODESEARCH_TERMINALS)
            return tree.child.nodeInPosition(state.random[thread].randint(0, self.terminals), GPNode.NODESEARCH_TERMINALS)
        else:
            if self.nonterminals == -1:
                self.nonterminals = tree.child.numNodes(GPNode.NODESEARCH_NONTERMINALS)
            if self.nonterminals > 0:
                return tree.child.nodeInPosition(state.random[thread].randint(0, self.nonterminals), GPNode.NODESEARCH_NONTERMINALS)
            else:
                return tree.child