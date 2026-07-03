from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DomainEvent:
    """Domain Event base class"""

    @property
    def qualname(self) -> str:
        """Returns the qualified name of the event class."""
        return self.__class__.__qualname__

    @property
    def full_qualname(self) -> str:
        """Returns the full qualified name of the event class (module + name)."""
        return f"{self.__module__}.{self.qualname}"


class DomainEventHandler[TEvent: DomainEvent](ABC):
    """Event Consumer generic class to handle Domain Events

    `TEvent` defines a subclass of `DomainEvent` that can be handled
    """

    @abstractmethod
    def process(self, event: TEvent, position: int, stream_id: UUID) -> None:
        """Process a Domain Event.

        Args:
            event: Domain Event to process.
            position: Event position in the Stream
            stream_id: Identifier of the emitter aggregate stream.

        Returns:
            None
        """
