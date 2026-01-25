from sharedkernel.domain.errors import SystemException


class InfrastructureException(SystemException):
    """Infrastructure Exception

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


class MapperNotFound(InfrastructureException):
    """MapperNotFound Exception

    Raised when no `EventMapper` was found in the `MappingPipeline` for a given event type.

    Args:
        event_type: Entity on which the error was raised.
    """

    def __init__(self, service: object, event_type: str):
        message = f"No Event Mapper was found for event {event_type}."
        super().__init__(type(service), message)


class UnsupportedEventHandler(InfrastructureException):
    """Exception raised when a service is trying to register an invalid event handler.

    Args:
        service: The service where the registration was attempted.
        handler: The name of the unsupported handler.
    """

    def __init__(self, service: object, handler: str):
        service_name = type(service).__name__
        message = f"`{handler}` cannot be registered to {service_name}"
        super().__init__(type(service), message)


class UnprocessableListener(InfrastructureException):
    """Exception raised when a listener cannot be processed (e.g., doesn't handle any events to subscribe to).

    Args:
        service: The service where the subscription was attempted.
        listener: The name of the unprocessable listener.
    """

    def __init__(self, service: object, listener: str):
        message = f"Cannot subscribe `{listener}` because it does not handle any event"
        super().__init__(type(service), message)


class IntegrityError(InfrastructureException):
    """IntegrityError defines an optimistic concurrency control error.

    Args:
        service: The service where the error occurred.
        entity_id: The identifier of the entity involved.
        position: The invalid event position.
        """
    def __init__(self, service: object, entity_id: str, position: int):
        message = f"Transaction concurrency control was invalid for Entity '{entity_id}' at position {position}."
        super().__init__(type(service), message)


class OutOfOrderEvent(InfrastructureException):
    """OutOfOrderEvent Exception marks when a domain event is received out of sequence.

    Args:
        service: The service where the error occurred.
        entity_id: The identifier of the entity involved.
        position: The out-of-order event position.
    """
    def __init__(self, service: object, entity_id: str, position: int):
        message = f"Event out of order received at position {position} for Projection '{entity_id}'."
        super().__init__(type(service), message)
