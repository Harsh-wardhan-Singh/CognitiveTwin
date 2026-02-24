from collections import deque


class DependencyPropagator:
    def __init__(self, concept_graph):
        """
        concept_graph: instance of ConceptGraph
        """
        self.graph = concept_graph

    def propagate(
        self,
        mastery_dict: dict,
        updated_concept: str,
        alpha: float = 0.08,
        decay_factor: float = 0.7,
        max_depth: int = 5
    ):
        """
        Propagates mastery changes through dependency graph.

        mastery_dict: {concept: mastery_value}
        updated_concept: concept that was directly updated
        alpha: base propagation rate
        decay_factor: decay multiplier per level
        max_depth: limit propagation depth for safety
        """

        if updated_concept not in mastery_dict:
            return mastery_dict

        queue = deque([(updated_concept, 0)])
        visited = set([updated_concept])

        while queue:
            current_concept, level = queue.popleft()

            if level >= max_depth:
                continue

            parent_mastery = mastery_dict.get(current_concept, 0.0)

            for child, weight in self.graph.children.get(current_concept, []):

                if child not in mastery_dict:
                    mastery_dict[child] = 0.0

                child_mastery = mastery_dict[child]

                # Distance-based decay
                influence_strength = alpha * (decay_factor ** level) * weight

                adjustment = influence_strength * (parent_mastery - child_mastery)

                new_mastery = child_mastery + adjustment

                # Clamp between 0 and 1
                mastery_dict[child] = min(max(new_mastery, 0.0), 1.0)

                if child not in visited:
                    visited.add(child)
                    queue.append((child, level + 1))

        return mastery_dict