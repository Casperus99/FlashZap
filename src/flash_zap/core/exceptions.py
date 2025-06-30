"""Custom exception classes for FlashZap."""

class InvalidFileError(Exception):
    """Raised when the imported file is invalid."""
    pass

class ValidationError(Exception):
    """Raised when data validation fails."""
    pass

class AIGraderError(Exception):
    """Raised when the AI grader service encounters an error."""
    pass 