from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import TypeVar, Generic


@dataclass(frozen=True)
class DomainEvent:
    """Domain Event base class"""


TEvent = TypeVar("TEvent", bound=DomainEvent)


class DomainEventHandler(ABC, Generic[TEvent]):
    """Event Consumer generic class to handle Domain Events

    `TEvent` defines a subclass of `DomainEvent` that can be handled
    """

    @abstractmethod
    def process(self, event: TEvent) -> None:
        """Process a Domain Event.

        Args:
            event: Domain Event to process.

        Returns:
            None
        """
