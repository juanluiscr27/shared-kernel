from dataclasses import dataclass
from functools import singledispatchmethod
from uuid import UUID

import pytest

from sharedkernel.domain.errors import UnknownEvent
from sharedkernel.domain.events import DomainEvent
from sharedkernel.infrastructure.data import DataModel
from sharedkernel.infrastructure.errors import OutOfOrderEvent
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
class UserLoggedIn(DomainEvent):
    name: str
    email: str


@dataclass(frozen=True)
class UserModel(DataModel):
    user_id: int
    name: str
    slug: str


class UserDetailsProjection(Projection[UserModel]):

    def get_position(self, entity_id: UUID, event_type: str) -> int:
        return 1

    def update_position(self, entity_id: UUID, event_type: str, position: int) -> None:
        print(f"{event_type} event processed by '{self.__class__.__name__}'")

    @singledispatchmethod
    def apply(self, event: DomainEvent) -> None:
        super().apply(event)

    @apply.register
    def _when(self, event: UserRegistered) -> None:
        pass

    @apply.register
    def _when(self, event: UserNameUpdated) -> None:
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

    projector = Projector(fake_logger, projection)

    # Act
    result = projector.handles

    # Assert
    assert result == expected


def test_projector_process_event_out_of_order_raise_error(fake_logger):
    # Arrange
    entity_id = UUID("018f55de-8321-7efd-a4e3-fcc2c5ec5eea")

    event = UserRegistered(user_id=101, name="John Doe", slug="john-doe")

    projection = UserDetailsProjection()

    projector = Projector(fake_logger, projection)

    # Act
    with pytest.raises(OutOfOrderEvent) as error:
        projector.process(event, position=3, entity_id=entity_id)

        # Assert
    assert str(error.value) == ("Event out of order received at position 3 for Projection "
                                "'018f55de-8321-7efd-a4e3-fcc2c5ec5eea'.")


def test_projector_process_already_applied_event(fake_logger, capture_stdout):
    # Arrange
    entity_id = UUID("018f55de-8321-7efd-a4e3-fcc2c5ec5eea")

    event = UserRegistered(user_id=101, name="John Doe", slug="john-doe")

    projection = UserDetailsProjection()

    projector = Projector(fake_logger, projection)

    # Act
    projector.process(event, position=1, entity_id=entity_id)

    # Assert
    assert not capture_stdout["console"]


def test_projector_process_unknown_event_raise_error(fake_logger):
    # Arrange
    entity_id = UUID("018f55de-8321-7efd-a4e3-fcc2c5ec5eea")

    event = UserLoggedIn(name="John Doe", email="john-doe@email.com")

    projection = UserDetailsProjection()

    projector = Projector(fake_logger, projection)

    # Act
    with pytest.raises(UnknownEvent) as error:
        projector.process(event, position=2, entity_id=entity_id)

        # Assert
    assert str(error.value) == "Event 'UserLoggedIn' cannot be applied to 'UserDetailsProjection'"
