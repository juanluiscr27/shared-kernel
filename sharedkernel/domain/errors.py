from dataclasses import asdict, dataclass
from typing import Any

from sharedkernel.domain.events import DomainEvent


class SystemException(Exception):
    """System Exception

    The base class for all other exceptions in the entire system.

    Args:
        message: Human readable string describing the exception.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class DomainException(SystemException):
    """Domain Exception

    Represents a violation to the business rule or domain logic constraints.

    Args:
        source: Entity or object on which the error was raised.
        message: Human readable string describing the exception.
        code: Identifies the problem type.
        reason: A human-readable explanation specific to this occurrence of the problem.
    """

    def __init__(self, source: object, message: str, code: str, reason: str) -> None:
        super().__init__(message)
        source_module = source.__module__
        source_name = source.__class__.__name__
        self.domain = f"{source_module}.{source_name}"
        self.code = code
        self.reason = reason


class UnhandledEventType(DomainException):
    """Unhandled Event Type Exception

    Thrown when an event is applied to an aggregate that does not correspond.

    Args:
        source: Entity on which the event invalid was applied.
        event: The event that is not handled by the entity.
    """

    def __init__(self, source: object, event: DomainEvent) -> None:
        event_name = type(event).__name__
        aggregate_name = type(source).__name__
        message = f"Event '{event_name}' cannot be applied to '{aggregate_name}'"
        reason = f"Aggregate '{aggregate_name}' does not handle event '{event_name}'"
        super().__init__(source, message, code="Aggregate.EventType.Unhandled", reason=reason)
        self.event = event


class EntityNotFound(DomainException):
    """Entity Not Found Exception

    Thrown when a command try to act on a resource that does not exist.
    This can occur when an entity is not found in the repository or is not part of an aggregate.

    Args:
        source: Cluster on which the entity was not found.
        message: Human readable string describing the exception.
        code: Identifies the problem type.
        reason: A human-readable explanation specific to this occurrence of the problem.
    """

    def __init__(self, source: object, message: str, code: str, reason: str) -> None:
        super().__init__(source, message, code=code, reason=reason)


class InvalidState(DomainException):
    """Invalid State Exception

    Thrown when the state of an entity is invalid for the operation being performed.
    This can occur when a business rule is violated or when the entity is in an inconsistent state.

    Args:
        source: Entity on which the invalid state was detected.
        message: Human readable string describing the exception.
        code: Identifies the problem type.
        reason: A human-readable explanation specific to this occurrence of the problem.
    """

    def __init__(self, source: object, message: str, code: str, reason: str) -> None:
        super().__init__(source, message, code=code, reason=reason)


class UniqueConstraintViolation(DomainException):
    """Unique Constraint Violation Exception

    Thrown when a unique constraint of an identity value is violated.
    This can occur when trying to create or update an entity with a value that already exists in the system.

    Args:
        source: Entity on which the unique constraint violation was detected.
        message: Human readable string describing the exception.
        code: Identifies the problem type.
        reason: A human-readable explanation specific to this occurrence of the problem.
    """

    def __init__(self, source: object, message: str, code: str, reason: str) -> None:
        super().__init__(source, message, code=code, reason=reason)


class ConcurrencyConflict(DomainException):
    """Concurrency Conflict Exception

    Thrown when an entity was modified by another transaction since it was read.
    This can occur when multiple transactions are trying to modify the same entity concurrently, leading to a conflict.

    Args:
        source: Entity with optimistic concurrency error.
        entity_id: The identifier of the entity with the conflict.
        version: The version of the entity when it was read.
    """

    def __init__(self, source: object, entity_id: Any, version: int) -> None:
        source_name = type(source).__name__
        message = f"Concurrency conflict for '{entity_id}' at version {version}"
        reason = f"Entity '{entity_id}' was modified by another transaction at version {version}"
        super().__init__(source, message, code=f"{source_name}.Conflict", reason=reason)


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
        """Converts the error model to a dictionary.

        Returns:
            A dictionary representation of the error.
        """
        return asdict(self)
