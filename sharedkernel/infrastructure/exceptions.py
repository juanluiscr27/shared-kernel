from typing import Any

from sharedkernel.domain.exceptions import SystemException


class InfrastructureException(SystemException):
    """Infrastructure Exception

    Represents an error that occurred during the interaction with external services.

    Args:
        source: Service on which the error was raised.
        message: Human readable string describing the exception.
    """

    def __init__(self, source: type, message: str) -> None:
        super().__init__(message)
        source_module = source.__module__
        source_name = source.__name__
        self.source = f"{source_module}.{source_name}"


class MapperNotFound(InfrastructureException):
    """MapperNotFound Exception

    Raised when no `EventMapper` was found in the `MappingPipeline` for a given event type.

    Args:
        source: Service where the mapper lookup failed.
        event_type: The event type that has no mapper.
    """

    def __init__(self, source: object, event_type: str) -> None:
        message = f"No Event Mapper was found for event {event_type}."
        super().__init__(type(source), message)


class UnsupportedEventHandler(InfrastructureException):
    """Exception raised when a service is trying to register an invalid event handler.

    Args:
        source: The service where the registration was attempted.
        handler: The name of the unsupported handler.
    """

    def __init__(self, source: object, handler: str) -> None:
        source_name = type(source).__name__
        message = f"`{handler}` cannot be registered to {source_name}"
        super().__init__(type(source), message)


class UnprocessableListener(InfrastructureException):
    """Exception raised when a listener cannot be processed (e.g., doesn't handle any events to subscribe to).

    Args:
        source: The service where the subscription was attempted.
        listener: The name of the unprocessable listener.
    """

    def __init__(self, source: object, listener: str) -> None:
        message = f"Cannot subscribe `{listener}` because it does not handle any event"
        super().__init__(type(source), message)


class IntegrityError(InfrastructureException):
    """IntegrityError defines an optimistic concurrency control error.

    Args:
        source: The service where the error occurred.
        entity_id: The identifier of the entity involved.
        position: The invalid event position.
        """
    def __init__(self, source: object, entity_id: Any, position: int) -> None:
        message = f"Transaction concurrency control was invalid for Entity '{entity_id}' at position {position}."
        super().__init__(type(source), message)


class EventOutOfSequence(InfrastructureException):
    """EventOutOfSequence Exception marks when a domain event is received out of sequence.

    Args:
        source: The service where the error occurred.
        entity_id: The identifier of the entity involved.
        position: The out-of-order event position.
    """
    def __init__(self, source: object, entity_id: Any, position: int) -> None:
        message = f"Event out of order received at position {position} for Projection '{entity_id}'."
        super().__init__(type(source), message)
