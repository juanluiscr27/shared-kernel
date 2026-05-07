from sharedkernel.domain.exceptions import SystemException


class ApplicationException(SystemException):
    """Application Exception

    Represents an error that occurred during the orchestration of the business logic.

    Args:
        source: Service on which the error was raised.
        message: Human readable string describing the exception.
    """

    def __init__(self, source: type, message: str) -> None:
        super().__init__(message)
        source_module = source.__module__
        source_name = source.__name__
        self.source = f"{source_module}.{source_name}"


class HandlerAlreadyRegistered(ApplicationException):
    """Raised when a handler is already registered for a request type."""

    def __init__(self, source: object, request_type: str) -> None:
        message = f"A Handler has been already registered for `{request_type}`"
        super().__init__(type(source), message)


class UnsupportedHandler(ApplicationException):
    """Raised when a handler type is not supported by the service bus."""

    def __init__(self, source: object, handler: str) -> None:
        source_name = type(source).__name__
        message = f"`{handler}` cannot be registered to {source_name}"
        super().__init__(type(source), message)
