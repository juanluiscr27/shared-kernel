from sharedkernel.domain.exceptions import SystemException


class ApiException(SystemException):
    """API Exception

    Represents an error that occurred when processing requests or returning responses.

    Args:
        source: Service on which the error was raised.
        message: Human readable string describing the exception.
    """

    def __init__(self, source: type, message: str) -> None:
        super().__init__(message)
        source_module = source.__module__
        source_name = source.__name__
        self.source = f"{source_module}.{source_name}"


class RequestMapperNotFound(ApiException):
    """Request MapperNotFound Exception

    Raised when no `RequestMapper` was found in the `MappingPipeline`.

    Args:
        source: Service where the mapper lookup failed.
        request: API Request trying to map.
    """

    def __init__(self, source: object, request: str) -> None:
        message = f"No Request Mapper was found for '{request}'."
        super().__init__(type(source), message)


class UnknownResponseModel(ApiException):
    """Unknown Response Model Exception

    Raised when the result of the execution from a Query or a Command cannot be mapped to `ResponseModel`.

    Args:
        source: Service where the mapping failed.
        response: Query or Command response.
    """

    def __init__(self, source: object, response: str) -> None:
        message = f"Unknown response model for '{response}'."
        super().__init__(type(source), message)
