from sharedkernel.domain.errors import ServiceError
from sharedkernel.infrastructure.errors import InfrastructureError


class ApiError(ServiceError):
    """API Error

    Represents an error that occurred when processing requests or returning responses.

    Args:
        service: Service on which the error was raised.
        message: Human readable string describing the exception.
    """

    def __init__(self, service: object, message: str):
        super().__init__(message)
        service_module = service.__module__
        service_name = service.__name__
        self.service = f"{service_module}.{service_name}"


class RequestMapperNotFound(ApiError):
    """Request MapperNotFound Error

    Raised when no `RequestMapper` was found in the `MappingPipeline`.

    Args:
        request: API Request trying to map.
    """

    def __init__(self, service: object, request: str):
        message = f"No Request Mapper was found for '{type(request).__name__}'."
        super().__init__(type(service), message)
