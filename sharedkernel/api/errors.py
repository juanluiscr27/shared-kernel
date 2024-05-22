from sharedkernel.infrastructure.errors import InfrastructureError


class RequestMapperNotFound(InfrastructureError):
    """Request MapperNotFound Error

    Raised when no `RequestMapper` was found in the `MappingPipeline`.

    Args:
        request: API Request trying to map.
    """

    def __init__(self, service: object, request: str):
        message = f"No Request Mapper was found for '{type(request).__name__}'."
        super().__init__(type(service), message)
