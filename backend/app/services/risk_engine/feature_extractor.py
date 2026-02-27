import numpy as np
from app.services.risk_engine.feature_schema import FEATURE_ORDER


class RiskFeatureExtractor:
    def __init__(self, concept_graph):
        self.graph = concept_graph

    def extract_features(
        self,
        mastery_dict: dict,
        confidence_metrics: dict,
        attempt_history: list,
        decay_deltas: dict
    ):
        concepts = list(mastery_dict.keys())
        mastery_values = np.array(list(mastery_dict.values()), dtype=np.float32)

        # -----------------------------
        # Layer 1: Mastery Signals
        # -----------------------------

        avg_mastery = np.mean(mastery_values)
        mastery_variance = np.var(mastery_values)
        low_mastery_ratio = np.mean(mastery_values < 0.4)

        depths = np.array(
            [self.graph.compute_depth(c) for c in concepts],
            dtype=np.float32
        )

        depth_sum = np.sum(depths) if np.sum(depths) > 0 else 1
        depth_weighted_mastery = np.sum(depths * mastery_values) / depth_sum

        # -----------------------------
        # Layer 2: Confidence Signals
        # -----------------------------

        avg_confidence = confidence_metrics.get("avg_confidence", 0.0)
        confidence_reliability = confidence_metrics.get("reliability", 0.0)
        overconfidence_score = confidence_metrics.get("overconfidence_score", 0.0)

        # -----------------------------
        # Layer 3: Temporal Signals
        # -----------------------------

        if attempt_history:
            recent_attempts = attempt_history[-10:]

            recent_correctness = np.array(
                [a["correct"] for a in recent_attempts],
                dtype=np.float32
            )

            times = np.array(
                [a.get("time_taken", 0.0) for a in recent_attempts],
                dtype=np.float32
            )

            retries = np.array(
                [a.get("retry_count", 0) for a in recent_attempts],
                dtype=np.float32
            )

            if len(recent_correctness) > 1:
                x = np.arange(len(recent_correctness))
                recent_accuracy_trend = np.polyfit(x, recent_correctness, 1)[0]
            else:
                recent_accuracy_trend = 0.0

            avg_time = np.mean(times)
            retry_rate = np.mean(retries > 0)
            avg_retry_count = np.mean(retries)

        else:
            recent_accuracy_trend = 0.0
            avg_time = 0.0
            retry_rate = 0.0
            avg_retry_count = 0.0

        decay_values = (
            np.array(list(decay_deltas.values()), dtype=np.float32)
            if decay_deltas else np.array([0.0], dtype=np.float32)
        )

        decay_vulnerability = np.mean(decay_values)

        # -----------------------------
        # Layer 4: Graph Signals
        # -----------------------------

        influence_scores = np.array(
            [self.graph.influence_score(c) for c in concepts],
            dtype=np.float32
        )

        avg_influence = np.mean(influence_scores)
        graph_density = self.graph.density()

        high_influence_threshold = (
            np.percentile(influence_scores, 75)
            if len(influence_scores) > 0 else 0
        )

        high_influence_low_mastery_count = np.sum(
            (influence_scores >= high_influence_threshold) &
            (mastery_values < 0.4)
        )

        # -----------------------------
        # Layer 5: Composite
        # -----------------------------

        bottleneck_risk_score = np.sum(
            influence_scores * (1 - mastery_values)
        )

        depth_weighted_weakness = np.sum(
            depths * (1 - mastery_values)
        )

        # -----------------------------
        # Final Vector
        # -----------------------------

        feature_vector = np.array([
            avg_mastery,
            mastery_variance,
            low_mastery_ratio,
            depth_weighted_mastery,
            avg_confidence,
            confidence_reliability,
            overconfidence_score,
            recent_accuracy_trend,
            decay_vulnerability,
            avg_time,
            retry_rate,
            avg_retry_count,
            high_influence_low_mastery_count,
            avg_influence,
            graph_density,
            bottleneck_risk_score,
            depth_weighted_weakness
        ], dtype=np.float32)

        metadata = dict(zip(FEATURE_ORDER, feature_vector))

        return feature_vector, metadata