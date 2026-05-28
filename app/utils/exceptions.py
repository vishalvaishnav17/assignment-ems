class ApplicationError(Exception):
    """Base exception class for all application errors."""

    status_code = 500

    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {"error": self.message}


class ResourceNotFoundError(ApplicationError):
    """Raised when a requested resource is not found (HTTP 404)."""

    status_code = 404


class ValidationError(ApplicationError):
    """Raised when request payload or data validation fails (HTTP 400)."""

    status_code = 400


class ConflictError(ApplicationError):
    """Raised when a unique database constraint or business logic conflict occurs (HTTP 409)."""

    status_code = 409
