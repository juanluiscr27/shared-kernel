from dataclasses import dataclass, asdict
from typing import Any

from sharedkernel.domain.events import DomainEvent


class ServiceError(Exception):
    """Service Error

    The base class for all other exceptions in the entire system.

    Args:
        message: Human readable string describing the exception.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DomainError(ServiceError):
    """Domain Error

    Represents a violation to the business rule or domain logic constraints.

    Args:
        entity: Entity on which the error was raised.
        message: Human readable string describing the exception.
    """

    def __init__(self, entity: object, message: str):
        super().__init__(message)
        entity_module = entity.__module__
        entity_name = entity.__class__.__name__
        self.domain = f"{entity_module}.{entity_name}"


class UnknownEvent(DomainError):
    """Unknown Event Error

    Thrown when an event is applied to an aggregate that does not correspond.

    Args:
        aggregate: Entity on which the event invalid was applied.
        event: The event that is not handled by the entity.
    """

    def __init__(self, aggregate: object, event: DomainEvent):
        event_name = type(event).__name__
        aggregate_name = type(aggregate).__name__
        message = f"Event '{event_name}' cannot be applied to '{aggregate_name}'"
        super().__init__(entity=aggregate, message=message)
        self.event = event


@dataclass(frozen=True)
class Error:
    """Error Model

    Represents an application error. Commonly used when a validation fails or
    an application rule is broken.

    Args:
        code: Identifies the problem type.
        message: A short summary to describe the type of problem in general.
        reason: A human-readable explanation specific to this occurrence of the problem.
        domain: A reference that identifies the specific instance where the problem occurred.
    """

    code: str
    message: str
    reason: str
    domain: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
