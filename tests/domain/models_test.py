from dataclasses import dataclass
from functools import singledispatchmethod

import pytest

from sharedkernel.domain.errors import UnknownEvent
from sharedkernel.domain.events import DomainEvent
from sharedkernel.domain.models import ValueObject, EntityID, Entity, Aggregate


@dataclass(frozen=True)
class Money(ValueObject):
    amount: float = 0
    currency: str = "USD"


@dataclass(frozen=True)
class CountryID(EntityID):
    value: str


class Country(Entity[CountryID]):

    def __init__(self, country_id: CountryID, name):
        super().__init__(country_id)
        self.name: str = name


@dataclass(frozen=True)
class UserID(EntityID):
    value: int


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    user_id: int
    name: str


@dataclass(frozen=True)
class UserNameUpdated(DomainEvent):
    user_id: int
    new_name: str


@dataclass(frozen=True)
class UserLoggedIn(DomainEvent):
    user_id: int
    name: str


class User(Aggregate[UserID]):

    def __init__(self, user_id: UserID, version: int, name: str):
        super().__init__(user_id, version)
        self.name = name

    @classmethod
    def load(cls, user_id: UserID, version: int, name: str, events: tuple):
        coach = cls(user_id=user_id, version=version, name=name)

        for event in events:
            coach._apply(event)

        return coach

    @classmethod
    def register(cls, user_id: UserID, name: str):
        user = cls(user_id=user_id, version=0, name=name)

        user_registered = UserRegistered(user_id=user_id.value, name=name)

        user._raise_event(user_registered)

        return user

    def update_name(self, name: str) -> None:
        name_updated = UserNameUpdated(user_id=self.id.value, new_name=name)

        self._raise_event(name_updated)

    @singledispatchmethod
    def _apply(self, event: DomainEvent) -> None:
        super()._apply(event)

    @_apply.register
    def _when(self, event: UserRegistered) -> None:
        self.name = event.name

    @_apply.register
    def _when(self, event: UserNameUpdated) -> None:
        self.name = event.new_name


def test_value_objects_with_same_value_are_equal():
    # Arrange
    expected = Money(10, "CAD")

    # Act
    result = Money(10, "CAD")

    # Assert
    assert result == expected


def test_value_objects_with_different_value_are_not_equal():
    # Arrange
    expected = Money(10, "CAD")

    # Act
    result = Money(20, "CAD")

    # Assert
    assert result != expected


def test_entities_with_same_id_are_equal():
    # Arrange
    country_id = CountryID("DO")

    # Act
    country1 = Country(country_id=country_id, name="Dominican Rep.")

    country2 = Country(country_id=country_id, name="Dominican Republic")

    # Assert
    assert country1 == country2


def test_entity_equal_to_value_object_is_false():
    # Arrange
    country_id1 = CountryID("DO")
    country_id2 = CountryID("DR")

    # Act
    country1 = Country(country_id=country_id1, name="Dominican Republic")

    # Assert
    assert (country1 == country_id2) is False


def test_entities_with_different_id_are_not_equal():
    # Arrange
    country_id1 = CountryID("DO")
    country_id2 = CountryID("DR")

    # Act
    country1 = Country(country_id=country_id1, name="Dominican Republic")

    country2 = Country(country_id=country_id2, name="Dominican Republic")

    # Assert
    assert country1 != country2


def test_entity_not_equal_to_value_object_is_true():
    # Arrange
    country_id1 = CountryID("DO")
    country_id2 = CountryID("DR")

    # Act
    country1 = Country(country_id=country_id1, name="Dominican Republic")

    # Assert
    assert country1 != country_id2


def test_entity_repr():
    # Arrange
    country_id = CountryID("DO")

    dr = Country(country_id=country_id, name="Dominican Republic")

    expected = "Country(id=CountryID(value='DO'))"

    # Act
    result = repr(dr)

    # Assert
    assert result == expected


def test_entity_is_hashable():
    # Arrange
    country_id = CountryID("DO")

    dr = Country(country_id=country_id, name="Dominican Republic")

    # Act
    result = {dr: True}

    # Assert
    assert result[dr]


def test_entity_qualname():
    # Arrange
    country_id = CountryID("DO")
    expected = "Country"

    # Act
    dr = Country(country_id=country_id, name="Dominican Republic")

    # Assert
    assert dr.qualname == expected


def test_entity_full_qualname():
    # Arrange
    country_id = CountryID("DO")
    expected = "tests.domain.models_test.Country"

    # Act
    dr = Country(country_id=country_id, name="Dominican Republic")

    # Assert
    assert dr.full_qualname == expected


def test_aggregates_with_same_id_are_equal():
    # Arrange
    user_id = UserID(101)

    # Act
    user1 = User(user_id=user_id, version=0, name="John Doe")

    user2 = User(user_id=user_id, version=0, name="John Doe Jr.")

    # Assert
    assert user1 == user2


def test_aggregates_with_different_id_are_not_equal():
    # Arrange
    user_id1 = UserID(101)
    user_id2 = UserID(102)

    # Act
    user1 = User(user_id=user_id1, version=0, name="John Doe")

    user2 = User(user_id=user_id2, version=0, name="John Doe")

    # Assert
    assert user1 != user2


def test_aggregates_version_number():
    # Arrange
    user_id = UserID(101)

    # Act
    user1 = User(user_id=user_id, version=1, name="John Doe")

    # Assert
    assert user1.version == 1


def test_aggregates_events_are_raised():
    # Arrange
    user_id = UserID(101)
    expected = UserRegistered(user_id=101, name="John Doe")

    # Act
    user = User.register(user_id=user_id, name="John Doe")

    result = user.changes[0]

    # Assert
    assert result == expected


def test_aggregates_events_are_applied():
    # Arrange
    user_id = UserID(101)
    user = User(user_id=user_id, version=1, name="John Doe")
    new_name = "John Doe Smith"

    # Act
    user.update_name(new_name)

    # Assert
    assert user.name == new_name


def test_aggregates_unknown_events_raise_error():
    # Arrange
    user_id = UserID(101)
    events = (UserLoggedIn(user_id=101, name="John Doe"),)

    expected = "Event 'UserLoggedIn' cannot be applied to 'User'"

    # Act
    with pytest.raises(UnknownEvent) as error:
        _ = User.load(user_id=user_id, version=1, name="John Doe", events=events)

    error_message = str(error.value)

    # Assert
    assert error_message == expected
