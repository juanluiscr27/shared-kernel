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
        service_name = service.__name__
        self.service = f"{service_module}.{service_name}"


class MapperNotFound(InfrastructureError):
    """MapperNotFound Error

    Raised when no `EventMapper` was found in the `MappingPipeline` for a given event type.

    Args:
        event_type: Entity on which the error was raised.
    """

    def __init__(self, service: object, event_type: str):
        message = f"No Event Mapper was found for event {event_type}."
        super().__init__(type(service), message)


class UnsupportedEventHandler(InfrastructureError):

    def __init__(self, service: object, handler: str):
        service_name = type(service).__name__
        message = f"`{handler}` cannot be registered to {service_name}"
        super().__init__(type(service), message)


class UnprocessableListener(InfrastructureError):

    def __init__(self, service: object, listener: str):
        message = f"Cannot subscribe `{listener}` because it does not handle any event"
        super().__init__(type(service), message)


class IntegrityError(InfrastructureError):

    def __init__(self, service: object, entity_id: str, position: int):
        message = f"Transaction concurrency control was invalid for Entity '{entity_id}' at position {position}."
        super().__init__(type(service), message)
