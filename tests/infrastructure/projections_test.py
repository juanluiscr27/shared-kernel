from dataclasses import dataclass
from functools import singledispatchmethod

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

    def process(self, event: DomainEvent, position: int) -> None:
        pass


def test_projector_handles_projection_events():
    # Arrange
    expected = ["tests.infrastructure.projections_test.UserRegistered",
                "tests.infrastructure.projections_test.UserNameUpdated"]

    projector = UserDetailsProjector()

    # Act
    result = projector.handles

    # Assert
    assert result == expected