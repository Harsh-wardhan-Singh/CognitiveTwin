from collections import defaultdict, deque


class ConceptGraph:
    def __init__(self):
        # Core structure
        self.parents = defaultdict(list)     # child -> [(parent, weight)]
        self.children = defaultdict(list)    # parent -> [(child, weight)]
        self.nodes = set()

        # Cached metrics
        self._depth_cache = {}
        self._influence_cache = {}
        self._topo_order = None

    # --------------------------------------------------
    # Core Graph Construction
    # --------------------------------------------------

    def add_concept(self, concept: str):
        self.nodes.add(concept)

    def add_prerequisite(self, parent: str, child: str, weight: float = 0.5):
        if parent == child:
            raise ValueError("Self-dependency is not allowed.")

        self.add_concept(parent)
        self.add_concept(child)

        # Prevent cycles
        if self._creates_cycle(parent, child):
            raise ValueError(f"Adding {parent} -> {child} creates a cycle.")

        self.children[parent].append((child, weight))
        self.parents[child].append((parent, weight))

        self._invalidate_cache()

    # --------------------------------------------------
    # Cycle Detection (DFS)
    # --------------------------------------------------

    def _creates_cycle(self, parent, child):
        visited = set()
        stack = [parent]

        while stack:
            node = stack.pop()
            if node == child:
                return True
            for next_node, _ in self.children.get(node, []):
                if next_node not in visited:
                    visited.add(next_node)
                    stack.append(next_node)
        return False

    # --------------------------------------------------
    # Basic Structural Metrics
    # --------------------------------------------------

    def in_degree(self, concept):
        return len(self.parents.get(concept, []))

    def out_degree(self, concept):
        return len(self.children.get(concept, []))

    def weighted_out_degree(self, concept):
        return sum(weight for _, weight in self.children.get(concept, []))

    def total_edges(self):
        return sum(len(v) for v in self.children.values())

    def density(self):
        n = len(self.nodes)
        if n <= 1:
            return 0
        return self.total_edges() / (n * (n - 1))

    # --------------------------------------------------
    # Depth Computation (Longest Prerequisite Chain)
    # --------------------------------------------------

    def compute_depth(self, concept):
        if concept in self._depth_cache:
            return self._depth_cache[concept]

        visited = set()

        def dfs(node):
            if node in visited:
                return 0
            visited.add(node)

            parents = self.parents.get(node, [])
            if not parents:
                return 0

            return 1 + max(dfs(p) for p, _ in parents)

        depth = dfs(concept)
        self._depth_cache[concept] = depth
        return depth

    # --------------------------------------------------
    # Downstream Influence
    # --------------------------------------------------

    def downstream_concepts(self, concept):
        if concept in self._influence_cache:
            return self._influence_cache[concept]

        visited = set()
        queue = deque([concept])

        while queue:
            node = queue.popleft()
            for child, _ in self.children.get(node, []):
                if child not in visited:
                    visited.add(child)
                    queue.append(child)

        self._influence_cache[concept] = visited
        return visited

    def influence_score(self, concept):
        return len(self.downstream_concepts(concept))

    # --------------------------------------------------
    # Topological Sort (Useful for Analytics + ML)
    # --------------------------------------------------

    def topological_sort(self):
        if self._topo_order is not None:
            return self._topo_order

        in_degree_map = {node: 0 for node in self.nodes}

        for parent in self.children:
            for child, _ in self.children[parent]:
                in_degree_map[child] += 1

        queue = deque([node for node in self.nodes if in_degree_map[node] == 0])
        topo_order = []

        while queue:
            node = queue.popleft()
            topo_order.append(node)

            for child, _ in self.children.get(node, []):
                in_degree_map[child] -= 1
                if in_degree_map[child] == 0:
                    queue.append(child)

        if len(topo_order) != len(self.nodes):
            raise ValueError("Graph contains a cycle.")

        self._topo_order = topo_order
        return topo_order

    # --------------------------------------------------
    # Global Graph Statistics (Future ML Features)
    # --------------------------------------------------

    def max_depth(self):
        return max((self.compute_depth(n) for n in self.nodes), default=0)

    def average_depth(self):
        if not self.nodes:
            return 0
        return sum(self.compute_depth(n) for n in self.nodes) / len(self.nodes)

    def average_influence(self):
        if not self.nodes:
            return 0
        return sum(self.influence_score(n) for n in self.nodes) / len(self.nodes)

    # --------------------------------------------------
    # Cache Invalidation
    # --------------------------------------------------

    def _invalidate_cache(self):
        self._depth_cache.clear()
        self._influence_cache.clear()
        self._topo_order = None