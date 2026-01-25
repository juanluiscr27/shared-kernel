from collections import deque
from dataclasses import dataclass
from typing import Deque, Generic, Tuple, TypeVar

from uuid import UUID

from sharedkernel.domain.events import DomainEvent
from sharedkernel.domain.errors import UnknownEvent


@dataclass(frozen=True)
class ValueObject:
    """Value Object base class

    Immutable object that represents a value in the domain with no identity.
    """


@dataclass(frozen=True)
class EntityID(ValueObject):
    """EntityID Value Object

    Represents the concept of a stringly typed ID to prevent primitive obsession.

    Args:
        value: The identification of primitive value that is wrapped up.
    """
    value: UUID


TId = TypeVar("TId", bound=EntityID)


class Entity(Generic[TId]):
    """Entity base class

    Object with an identity relevant to the domain and a set of attributes that define its state.

    Args:
        entity_id: A strongly typed Entity identifier.
    """

    def __init__(self, entity_id: TId) -> None:
        self._id = entity_id

    @property
    def id(self) -> TId:
        """A strongly typed entity identifier."""
        return self._id

    @property
    def qualname(self) -> str:
        """Returns the qualified name of the entity class."""
        return self.__class__.__qualname__

    @property
    def full_qualname(self) -> str:
        """Returns the full qualified name of the entity class (module + name)."""
        return f"{self.__module__}.{self.qualname}"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._id})"

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self._id == other.id
        else:
            return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        else:
            return not result

    def __hash__(self):
        return hash((self.__class__, self._id))


class Aggregate(Entity[TId]):
    """Aggregate base class

    A cluster of domain objects that can be treated as a single unit. An aggregate defines a transactional
    consistency boundary. An aggregate has a root entity which is responsible for enforcing the invariants of the
    aggregate, which ensure the business rules and protect the data integrity.

    Args:
        entity_id: A strongly typed Entity identifier.
        version: Aggregate version number
    """

    def __init__(self, entity_id: TId, version: int) -> None:
        super().__init__(entity_id)
        self._version = version
        self._events: Deque[DomainEvent] = deque()

    @property
    def version(self) -> int:
        """The current version of the aggregate."""
        return self._version

    @property
    def changes(self) -> Tuple[DomainEvent, ...]:
        """A tuple containing all the domain events that have occurred in the aggregate."""
        return tuple(self._events)

    def _apply(self, event: DomainEvent) -> None:
        """Applies a domain event to the aggregate to change its state.

        Args:
            event: The domain event to apply.

        Raises:
            UnknownEvent: If the event is not handled by the aggregate.
        """
        raise UnknownEvent(self, event)

    def _raise_event(self, event: DomainEvent) -> None:
        """Raises a domain event, applying it to the aggregate and adding it to the changes' collection.

        Args:
            event: The domain event to raise.
        """
        self._apply(event)
        self._events.append(event)

    def clear_events(self) -> None:
        """Clears all the domain events in the aggregate."""
        self._events.clear()
