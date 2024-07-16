from dataclasses import dataclass
from functools import singledispatchmethod
from uuid import UUID

from sharedkernel.domain.events import DomainEvent
from sharedkernel.infrastructure.data import DataModel
from sharedkernel.infrastructure.projections import Projection, Projector


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    user_id: int
    name: str
    slug: str


@dataclass(frozen=True)
class UserNameUpdated(DomainEvent):
    user_id: int
    new_name: str
    previous_name: str


@dataclass(frozen=True)
class UserModel(DataModel):
    user_id: int
    name: str
    slug: str


class UserDetailsProjection(Projection[UserModel]):

    def get_position(self, entity_id: UUID, event_type: str) -> int:
        return 1

    def update_position(self, entity_id: UUID, event_type: str, position: int) -> None:
        pass

    @singledispatchmethod
    def apply(self, event: DomainEvent) -> None:
        super().apply(event)

    @apply.register
    def _when(self, event: UserRegistered) -> None:
        pass

    @apply.register
    def _when(self, event: UserNameUpdated) -> None:
        pass


class UserDetailsProjector(Projector[UserDetailsProjection]):

    def process(self, event: DomainEvent, position: int, version: int) -> None:
        pass


def test_projection_type():
    # Arrange
    expected = "UserModel"

    projection = UserDetailsProjection()

    # Act
    result = projection.model_type

    # Assert
    assert result == expected


def test_projector_handles_projection_events(fake_logger):
    # Arrange
    expected = ["UserRegistered", "UserNameUpdated"]

    projection = UserDetailsProjection()

    projector = UserDetailsProjector(fake_logger, projection)

    # Act
    result = projector.handles

    # Assert
    assert result == expected
