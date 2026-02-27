"""
Service Container for Dependency Injection
Centralizes instantiation of all services and engines
"""

from typing import Optional
from sqlalchemy.orm import Session
import os

from app.services.cognitive_engine.pipeline import CognitivePipeline
from app.services.cognitive_engine.concept_graph import ConceptGraph
from app.services.ai_generation.explanation_generator import ExplanationGenerator
from app.services.analytics.insight_generator import InsightGenerator
from app.services.core.submission_controller import SubmissionController
from app.services.persistence.mastery_repository import MasteryRepository
from app.services.persistence.attempt_repository import AttemptRepository
from app.core.exceptions import PipelineError


class ServiceContainer:
    """
    Global service container.
    Singleton pattern - instantiates once per app lifecycle.
    """

    def __init__(self, db: Session):
        self.db = db
        self._pipeline: Optional[CognitivePipeline] = None
        self._concept_graph: Optional[ConceptGraph] = None
        self._explanation_generator: Optional[ExplanationGenerator] = None
        self._insight_generator: Optional[InsightGenerator] = None
        self._submission_controller: Optional[SubmissionController] = None
        self._mastery_repository: Optional[MasteryRepository] = None
        self._training_data_store: list = []  # In-memory for now

    @property
    def concept_graph(self) -> ConceptGraph:
        """Lazy load concept graph"""
        if self._concept_graph is None:
            self._concept_graph = ConceptGraph()
        return self._concept_graph

    @property
    def explanation_generator(self) -> ExplanationGenerator:
        """Lazy load explanation generator"""
        if self._explanation_generator is None:
            try:
                self._explanation_generator = ExplanationGenerator()
            except Exception:
                # Gracefully handle LLM client initialization failure
                self._explanation_generator = None
        return self._explanation_generator

    @property
    def insight_generator(self) -> InsightGenerator:
        """Lazy load insight generator"""
        if self._insight_generator is None:
            self._insight_generator = InsightGenerator()
        return self._insight_generator

    @property
    def mastery_repository(self) -> MasteryRepository:
        """Get mastery repository"""
        return MasteryRepository()

    @property
    def pipeline(self) -> CognitivePipeline:
        """
        Lazy load the complete cognitive pipeline.
        This is the core AI engine orchestrator.
        """
        if self._pipeline is None:
            try:
                risk_model_path = os.getenv(
                    "RISK_MODEL_PATH",
                    "app/services/risk_engine/models/risk_model.joblib"
                )

                self._pipeline = CognitivePipeline(
                    graph=self.concept_graph,
                    risk_model_path=risk_model_path,
                    training_data_store=self._training_data_store,
                    db=self.db
                )
            except Exception as e:
                raise PipelineError(f"Failed to initialize cognitive pipeline: {str(e)}")

        return self._pipeline

    @property
    def submission_controller(self) -> SubmissionController:
        """
        Lazy load submission controller.
        This orchestrates quiz submission processing.
        """
        if self._submission_controller is None:
            self._submission_controller = SubmissionController(
                cognitive_pipeline=self.pipeline,
                training_store=self._training_data_store
            )
        return self._submission_controller

    def reset_pipeline(self):
        """Reset pipeline (useful for testing or model reloads)"""
        self._pipeline = None
        self._concept_graph = None


# Global container instance
_service_container: Optional[ServiceContainer] = None


def get_service_container(db: Session) -> ServiceContainer:
    """
    Get or initialize the global service container.
    Call this in your FastAPI dependency to get access to all services.
    """
    global _service_container
    if _service_container is None:
        _service_container = ServiceContainer(db)
    return _service_container


def reset_service_container():
    """Reset the service container (for testing)"""
    global _service_container
    _service_container = None

