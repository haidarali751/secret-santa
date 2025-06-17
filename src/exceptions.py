class SecretSantaError(Exception):
    """Base exception for Secret Santa assignment system."""
    pass


class InputFileError(SecretSantaError):
    """Raised when there are issues with input files."""
    pass


class AssignmentError(SecretSantaError):
    """Raised when there are issues with Secret Santa assignments."""
    pass


class ValidationError(SecretSantaError):
    """Raised when input data validation fails."""
    pass 