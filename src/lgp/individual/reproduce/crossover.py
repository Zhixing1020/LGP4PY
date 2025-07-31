from src.ec.breeding_pipeline import BreedingPipeline

class CrossoverPipeline(BreedingPipeline):
    P_NUM_TRIES = "tries"
    P_MAXDEPTH = "maxdepth"
    P_MAXSIZE = "maxsize"
    P_CROSSOVER = "xover"
    P_TOSS = "toss"
    INDS_PRODUCED = 2
    NUM_SOURCES = 2
    NO_SIZE_LIMIT = -1
    TREE_UNFIXED = -1

    def __init__(self):
        super().__init__()
        self.nodeselect1 = None
        self.nodeselect2 = None
        self.tree1 = self.TREE_UNFIXED
        self.tree2 = self.TREE_UNFIXED
        self.numTries = 1
        self.maxDepth = 1
        self.maxSize = self.NO_SIZE_LIMIT
        self.tossSecondParent = False
        self.parents = [None, None]

    def default_base(self):
        return GPKozaDefaults.base().push(self.P_CROSSOVER)

    def num_sources(self):
        return self.NUM_SOURCES

    def setup(self, state, base):
        super().setup(state, base)

        def_base = self.default_base()

        p0 = base.push("nodeselector").push("0")
        d0 = def_base.push("nodeselector").push("0")
        self.nodeselect1 = state.parameters.get_instance_for_parameter(p0, d0, GPNodeSelector)
        self.nodeselect1.setup(state, p0)

        p1 = base.push("nodeselector").push("1")
        d1 = def_base.push("nodeselector").push("1")
        if state.parameters.exists(p1, d1) and state.parameters.get_string(p1, d1) == "same":
            self.nodeselect2 = self.nodeselect1.clone()
        else:
            self.nodeselect2 = state.parameters.get_instance_for_parameter(p1, d1, GPNodeSelector)
            self.nodeselect2.setup(state, p1)

        self.numTries = state.parameters.get_int(base.push(self.P_NUM_TRIES), def_base.push(self.P_NUM_TRIES), 1)
        if self.numTries <= 0:
            state.output.fatal("Invalid number of crossover tries.")

        self.maxDepth = state.parameters.get_int(base.push(self.P_MAXDEPTH), def_base.push(self.P_MAXDEPTH), 1)
        if self.maxDepth <= 0:
            state.output.fatal("Invalid crossover max depth.")

        if state.parameters.exists(base.push(self.P_MAXSIZE), def_base.push(self.P_MAXSIZE)):
            self.maxSize = state.parameters.get_int(base.push(self.P_MAXSIZE), def_base.push(self.P_MAXSIZE), 1)
            if self.maxSize < 1:
                state.output.fatal("Invalid crossover max size.")

        if state.parameters.exists(base.push("tree").push("0"), def_base.push("tree").push("0")):
            self.tree1 = state.parameters.get_int(base.push("tree").push("0"), def_base.push("tree").push("0"), 0)

        if state.parameters.exists(base.push("tree").push("1"), def_base.push("tree").push("1")):
            self.tree2 = state.parameters.get_int(base.push("tree").push("1"), def_base.push("tree").push("1"), 0)

        self.tossSecondParent = state.parameters.get_boolean(base.push(self.P_TOSS), def_base.push(self.P_TOSS), False)


    def verifyPoints(self, initializer, inner1, inner2):
        if not inner1.swapCompatibleWith(initializer, inner2):
            return False

        if inner1.depth() + inner2.atDepth() > self.maxDepth:
            return False

        if self.maxSize != self.NO_SIZE_LIMIT:
            inner1size = inner1.numNodes()
            inner2size = inner2.numNodes()
            if inner1size > inner2size:
                root2 = inner2.rootParent().child
                root2size = root2.numNodes()
                if root2size - inner2size + inner1size > self.maxSize:
                    return False

        return True

    def produce(self, min, max, start, subpopulation, inds, state, thread):
        n = self.typicalIndsProduced()
        if n < min:
            n = min
        if n > max:
            n = max

        if not state.random[thread].random() < self.likelihood:
            return self.reproduce(n, start, subpopulation, inds, state, thread, True)

        q = start
        while q < n + start:
            if self.sources[0] == self.sources[1]:
                self.sources[0].produce(2, 2, 0, subpopulation, self.parents, state, thread)
            else:
                self.sources[0].produce(1, 1, 0, subpopulation, self.parents, state, thread)
                self.sources[1].produce(1, 1, 1, subpopulation, self.parents, state, thread)

            parent1 = self.parents[0]
            parent2 = self.parents[1]

            q += self.produce_individuals(min, max, q, subpopulation, inds, state, thread, [parent1, parent2])

        return n

    def produce_individuals(self, min, max, start, subpopulation, inds, state, thread, parents):
        # Placeholder for actual logic to create offspring via crossover
        # Should clone, select crossover points, verify, and swap subtrees
        # This is where the second half of the original Java logic would go
        return self.INDS_PRODUCED if not self.tossSecondParent else 1