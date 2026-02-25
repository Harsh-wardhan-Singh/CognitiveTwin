from datetime import datetime
from typing import Dict, Any

from cognitive_engine.mastery_update import MasteryUpdater
from cognitive_engine.retention_decay import RetentionDecay
from cognitive_engine.dependency_propagation import DependencyPropagator
from cognitive_engine.confidence_model import ConfidenceModel

from risk_engine.feature_extractor import RiskFeatureExtractor
from risk_engine.predictor import RiskPredictor

from analytics.class_risk_aggregator import ClassRiskAggregator
from analytics.heatmap_builder import HeatmapBuilder
from analytics.insight_generator import InsightGenerator


class CognitivePipeline:
    """
    Full intelligence pipeline:

    Quiz Submission →
    Decay →
    BKT Update →
    Confidence →
    Propagation →
    Risk →
    Analytics →
    Training Data Storage
    """

    def __init__(
        self,
        graph,
        risk_model_path: str,
        training_data_store: list  # in-memory for now (replace with DB later)
    ):
        self.mastery_updater = MasteryUpdater()
        self.decay_engine = RetentionDecay()
        self.propagator = DependencyPropagator(graph)
        self.confidence_model = ConfidenceModel()

        self.feature_extractor = RiskFeatureExtractor(graph)
        self.risk_predictor = RiskPredictor(risk_model_path)

        self.class_risk_aggregator = ClassRiskAggregator()
        self.heatmap_builder = HeatmapBuilder()
        self.insight_generator = InsightGenerator()

        self.training_data_store = training_data_store  # stored for overnight retrain


    def process_submission(
        self,
        student_state,
        concept: str,
        correct: bool,
        response_time: float,
        student_confidence: float,
        total_attempts: int,
        class_states: Dict[str, Any]
    ) -> Dict[str, Any]:

        now = datetime.now()

        old_mastery_snapshot = student_state.mastery_dict.copy()

        # ---------------------------
        # 1️⃣ Apply Decay to All Concepts
        # ---------------------------
        for c in student_state.mastery_dict:
            last_time = student_state.last_attempt_time.get(c)
            if last_time:
                student_state.mastery_dict[c] = self.decay_engine.apply_decay(
                    student_state.mastery_dict[c],
                    last_time,
                    now
                )

        # ---------------------------
        # 2️⃣ Apply BKT Update
        # ---------------------------
        updated_mastery = self.mastery_updater.update(
            prior=student_state.mastery_dict.get(concept, 0.5),
            correct=correct,
            confidence=student_confidence
        )

        student_state.mastery_dict[concept] = updated_mastery

        # ---------------------------
        # 3️⃣ Update Attempt History
        # ---------------------------
        student_state.attempt_history.setdefault(concept, []).append(correct)
        student_state.last_attempt_time[concept] = now

        # ---------------------------
        # 4️⃣ Confidence Recalculation
        # ---------------------------
        confidence_score = self.confidence_model.compute(
            student_state.attempt_history[concept]
        )

        student_state.confidence_metrics[concept] = confidence_score

        # ---------------------------
        # 5️⃣ Dependency Propagation
        # ---------------------------
        self.propagator.propagate(
            mastery_dict=student_state.mastery_dict,
            updated_concept=concept
        )

        # ---------------------------
        # 6️⃣ Risk Feature Extraction
        # ---------------------------
        feature_vector = self.feature_extractor.extract(
            mastery_dict=student_state.mastery_dict,
            attempt_history=student_state.attempt_history,
            confidence_metrics=student_state.confidence_metrics,
            decay_deltas=student_state.compute_decay_deltas(),
            total_attempts=total_attempts
        )

        risk_prediction = self.risk_predictor.predict(feature_vector)

        student_state.risk_profile = risk_prediction

        # ---------------------------
        # 7️⃣ Store Training Data (For Manual Overnight Retrain)
        # ---------------------------
        self.training_data_store.append({
            "features": feature_vector,
            "label": risk_prediction["risk_label"],  # later can replace with real outcome
            "timestamp": now.isoformat()
        })

        # ---------------------------
        # 8️⃣ Analytics Integration
        # ---------------------------
        class_risk = self.class_risk_aggregator.aggregate(class_states)

        heatmap = self.heatmap_builder.build(class_states)

        insights = self.insight_generator.generate(
            student_state=student_state,
            class_states=class_states
        )

        # ---------------------------
        # 9️⃣ Delta Snapshot (Teacher Real-Time View)
        # ---------------------------
        mastery_delta = {
            c: student_state.mastery_dict[c] - old_mastery_snapshot.get(c, 0)
            for c in student_state.mastery_dict
        }

        return {
            "updated_mastery": student_state.mastery_dict,
            "mastery_delta": mastery_delta,
            "risk": risk_prediction,
            "confidence": student_state.confidence_metrics,
            "class_risk": class_risk,
            "heatmap": heatmap,
            "insights": insights
        }