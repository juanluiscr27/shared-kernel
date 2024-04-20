from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic


@dataclass(frozen=True)
class IntegrationEvent:
    """Integration Event base class

    Integration events are used for sharing domain state across multiple bounded context or external systems.
    """


TIEvent = TypeVar("TIEvent", bound=IntegrationEvent)


class IntegrationEventHandler(ABC, Generic[TIEvent]):
    """Event Consumer generic class to handle Integration Events.

    `TIEvent` defines a subclass of `IntegrationEvent` that can be handled.
    """

    @abstractmethod
    def process(self, event: TIEvent) -> None:
        """Process an Integration Event.

        Args:
            event: Integration Event to process.

        Returns:
            None
        """
