class LLMTransportError(Exception):
    """Raised when LLM transport fails after retries."""
    pass


class SchemaValidationError(Exception):
    """Raised when generated content fails schema validation."""
    pass


class GenerationFailure(Exception):
    """Raised when generation repeatedly fails."""
    pass