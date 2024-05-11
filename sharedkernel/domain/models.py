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
    def id(self):
        return self._id

    @property
    def qualname(self):
        return self.__class__.__qualname__

    @property
    def full_qualname(self):
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
        return self._version

    @property
    def changes(self) -> Tuple[DomainEvent, ...]:
        return tuple(self._events)

    def _apply(self, event: DomainEvent) -> None:
        raise UnknownEvent(self, event)

    def _raise_event(self, event: DomainEvent) -> None:
        self._events.append(event)

    def clear_events(self) -> None:
        self._events.clear()
