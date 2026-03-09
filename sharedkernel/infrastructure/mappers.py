from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime
from types import get_original_bases
from typing import Any, get_args
from uuid import UUID

from sharedkernel.domain.events import DomainEvent
from sharedkernel.infrastructure.data import Event


# noinspection PyUnusedLocal
def to_event(message: dict[str, Any], context: Any) -> Event:  # noqa: ARG001
    """Converts a raw message dictionary to an Event data model.

    Args:
        message: The raw message dictionary.
        context: Optional context for mapping.

    Returns:
        A populated Event instance.
    """
    return Event(
        event_id=UUID(message['id']),
        event_type=message['type'],
        position=message['position'],
        data=message['data'],
        stream_id=UUID(message['stream_id']),
        stream_type=message['stream_type'],
        version=message['version'],
        created=datetime.fromisoformat(message['created']),
        correlation_id=UUID(message['correlation_id']),
    )


class Mapper[TEvent: DomainEvent](ABC):
    """Base class for event mappers.

    Implementations should define how to map a dictionary of data into a specific TEvent.
    """

    def __init__(self) -> None:
        self._next: Mapper[Any] | None = None

    @property
    def event_type(self) -> str:
        """Returns the name of the event type this mapper handles."""
        bases = get_original_bases(self.__class__)
        args = get_args(bases[0])
        return args[0].__name__

    def set_next(self, mapper: "Mapper[Any]") -> None:
        """Sets the next mapper in the chain.

        Args:
            mapper: The next mapper instance.
        """
        self._next = mapper

    @abstractmethod
    def map(self, data: dict[str, Any], event_type: str) -> TEvent | None:
        """Maps raw data to a domain event if the type matches.

        Args:
            data: The raw event data dictionary.
            event_type: The type name of the event.

        Returns:
            The mapped domain event, or None if the type does not match.
        """
        ...

    def map_next(self, data: dict[str, Any], event_type: str) -> DomainEvent | None:
        """Delegates mapping to the next mapper in the chain.

        Args:
            data: The raw event data dictionary.
            event_type: The type name of the event.

        Returns:
            The result of the next mapper, or None if no next mapper exists.
        """
        if not self._next:
            return None

        return self._next.map(data, event_type)


class MappingBehavior(ABC):
    """Abstract base class defining event mapping behavior."""

    @abstractmethod
    def map(self, data: dict[str, Any], event_type: str) -> DomainEvent | None:
        """Maps raw data to a domain event.

        Args:
            data: The raw event data dictionary.
            event_type: The type name of the event.

        Returns:
            The mapped domain event or None.
        """
        ...


class MappersChain(MappingBehavior):
    """A chain of mappers that attempts to map an event using each mapper in sequence."""

    def __init__(self) -> None:
        self._mappers: deque[Mapper[Any]] = deque()
        self._first: Mapper[Any] | None = None

    def add(self, mapper: Mapper[Any]) -> None:
        """Adds a mapper to the beginning of the chain.

        Args:
            mapper: The mapper instance to add.
        """
        if self._first:
            mapper.set_next(self._first)

        self._mappers.appendleft(mapper)
        self._first = mapper

    def map(self, data: dict[str, Any], event_type: str) -> DomainEvent | None:
        """Attempts to map the event by passing it through the chain.

        Args:
            data: The raw event data dictionary.
            event_type: The type name of the event.

        Returns:
            The first non-None result from the chain, or None if all fail.
        """
        if not self._first:
            return None

        return self._first.map(data, event_type)


class MappingPipeline:
    """A pipeline for registering and executing multiple mapping behaviors."""

    def __init__(self) -> None:
        self._chain: list[MappingBehavior] = []

    def register(self, behavior: MappingBehavior) -> None:
        """Registers a mapping behavior in the pipeline.

        Args:
            behavior: The mapping behavior instance.
        """
        self._chain.append(behavior)

    def map(self, data: dict[str, Any], event_type: str) -> DomainEvent | None:
        """Executes the pipeline by calling each registered behavior until one returns a domain event.

        Args:
            data: The raw event data dictionary.
            event_type: The type name of the event.

        Returns:
            The first successfully mapped domain event, or None.
        """
        for behavior in self._chain:
            event = behavior.map(data, event_type)

            if event:
                return event

        return None
