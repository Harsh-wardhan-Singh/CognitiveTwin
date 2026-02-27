"""
Core exception classes for the cognitive twin system.
All services should raise these exceptions for consistent error handling.
"""

class CognitiveException(Exception):
    """Base exception for all cognitive twin errors"""
    def __init__(self, message: str, error_code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationError(CognitiveException):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class PipelineError(CognitiveException):
    """Raised when pipeline processing fails"""
    def __init__(self, message: str):
        super().__init__(message, "PIPELINE_ERROR")


class MasteryUpdateError(CognitiveException):
    """Raised when mastery update fails"""
    def __init__(self, message: str):
        super().__init__(message, "MASTERY_UPDATE_ERROR")


class RiskPredictionError(CognitiveException):
    """Raised when risk prediction fails"""
    def __init__(self, message: str):
        super().__init__(message, "RISK_PREDICTION_ERROR")


class QuizSelectionError(CognitiveException):
    """Raised when quiz selection fails"""
    def __init__(self, message: str):
        super().__init__(message, "QUIZ_SELECTION_ERROR")


class RepositoryError(CognitiveException):
    """Raised when database operations fail"""
    def __init__(self, message: str):
        super().__init__(message, "REPOSITORY_ERROR")


class NotFoundError(CognitiveException):
    """Raised when requested resource is not found"""
    def __init__(self, resource_type: str, resource_id):
        message = f"{resource_type} not found: {resource_id}"
        super().__init__(message, "NOT_FOUND_ERROR")


class UnauthorizedError(CognitiveException):
    """Raised when user is not authorized"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, "UNAUTHORIZED_ERROR")


class AIGenerationError(CognitiveException):
    """Raised when AI content generation fails"""
    def __init__(self, message: str):
        super().__init__(message, "AI_GENERATION_ERROR")
