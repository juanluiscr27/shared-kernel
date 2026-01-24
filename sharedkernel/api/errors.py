from sharedkernel.domain.errors import SystemException


class ApiException(SystemException):
    """API Exception

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


class RequestMapperNotFound(ApiException):
    """Request MapperNotFound Exception

    Raised when no `RequestMapper` was found in the `MappingPipeline`.

    Args:
        request: API Request trying to map.
    """

    def __init__(self, service: object, request: str):
        message = f"No Request Mapper was found for '{request}'."
        super().__init__(type(service), message)


class UnknownResponseModel(ApiException):
    """Unknown Response Model Exception

    Raised when the result of the execution from a Query or a Command cannot be mapped to `ResponseModel`.

    Args:
        response: Query or Command response.
    """

    def __init__(self, service: object, response: str):
        message = f"Unknown response model for '{response}'."
        super().__init__(type(service), message)
