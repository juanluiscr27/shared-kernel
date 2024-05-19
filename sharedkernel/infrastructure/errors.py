from sharedkernel.domain.errors import ServiceError


class InfrastructureError(ServiceError):
    """Infrastructure Error

    Represents an error that occurred during the interaction with external services.

    Args:
        service: Service on which the error was raised.
        message: Human readable string describing the exception.
    """

    def __init__(self, service: object, message: str):
        super().__init__(message)
        service_module = service.__module__
        service_name = service.__class__.__name__
        self.service = f"{service_module}.{service_name}"


class MapperNotFound(InfrastructureError):
    """MapperNotFound Error

    Raised when no `EventMapper` was found in the `MappingPipeline` for a given event type.

    Args:
        event_type: Entity on which the error was raised.
    """

    def __init__(self, service: object, event_type: str):
        message = f"No Event Mapper was found for event {event_type}."
        super().__init__(service, message)
