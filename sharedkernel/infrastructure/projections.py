from logging import Logger
from abc import abstractmethod, ABC
from types import get_original_bases
from typing import TypeVar, Generic, List, get_args
from uuid import UUID

from typeinspection import get_handled_types

from sharedkernel.domain.errors import UnknownEvent
from sharedkernel.domain.events import DomainEvent
from sharedkernel.infrastructure.data import DataModel
from sharedkernel.infrastructure.errors import OutOfOrderEvent

TModel = TypeVar("TModel", bound=DataModel)


class Projection(ABC, Generic[TModel]):
    """Base class for projections.

    A projection is responsible for transforming a stream of events into a read-optimized data model.
    """

    @property
    def model_type(self) -> str:
        """Returns the name of the model type this projection is based on."""
        bases = get_original_bases(self.__class__)
        args = get_args(bases[0])
        return args[0].__name__

    @abstractmethod
    def get_position(self, entity_id: UUID, event_type: str) -> int:
        """Retrieves the last applied event position for this projection.

        Args:
            entity_id: The identifier of the projected entity.
            event_type: The type name of the event.

        Returns:
            The last recorded position.
        """
        ...

    def apply(self, event: DomainEvent) -> None:
        """Applies a domain event to the projection.

        Args:
            event: The domain event to apply.

        Raises:
            UnknownEvent: If the event is not handled by the projection.
        """
        raise UnknownEvent(self, event)

    @abstractmethod
    def update_position(self, entity_id: UUID, event_type: str, position: int) -> None:
        """Updates the recorded position for this projection.

        Args:
            entity_id: The identifier of the projected entity.
            event_type: The type name of the event.
            position: The new sequential position.
        """
        ...


TProjection = TypeVar("TProjection", bound=Projection)


class Projector(Generic[TProjection]):
    """Wraps a Projection to handle event processing logic, including out-of-order detection.
    
    Args:
        logger: The logger to use for logging.
        projection: The projection to wrap.
    """

    def __init__(self, logger: Logger, projection: Projection):
        self._logger = logger
        self.projection = projection

    @property
    def handles(self) -> List[str]:
        """Returns a list of event names that this projector handles."""
        return get_handled_types(type(self.projection))

    def process(self, event: DomainEvent, position: int, entity_id: UUID) -> None:
        """Processes a domain event by applying it to the projection and updating the position.

        Args:
            event: The domain event to process.
            position: The sequential position of the event in the stream.
            entity_id: The identifier of the entity the event belongs to.

        Raises:
            OutOfOrderEvent: If the event is out of sequence.
        """
        current_position = self.projection.get_position(entity_id, event.qualname)

        event_type = event.qualname
        if position < current_position + 1:
            self._logger.debug(f"{event_type} position {position} has been already applied to Projection {entity_id}")
            return

        if position > current_position + 1:
            self._logger.error(f"{event_type} position {position} is out of order in Projection {entity_id}")
            raise OutOfOrderEvent(self.projection, str(entity_id), position)

        self.projection.apply(event)
        self._logger.info(f"{event_type} position {position} has been projected to record {entity_id}")

        self.projection.update_position(entity_id, event_type, position)
        self._logger.debug(f"{event_type} at Projection {entity_id} has been updated to position {position}")
