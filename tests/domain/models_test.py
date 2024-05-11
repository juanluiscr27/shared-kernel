from dataclasses import dataclass

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


class User(Aggregate[UserID]):

    def __init__(self, user_id: UserID, name):
        super().__init__(user_id, 0)
        self.name: str = name


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


def test_entities_with_different_id_are_not_equal():
    # Arrange
    country_id1 = CountryID("DO")
    country_id2 = CountryID("DR")

    # Act
    country1 = Country(country_id=country_id1, name="Dominican Republic")

    country2 = Country(country_id=country_id2, name="Dominican Republic")

    # Assert
    assert country1 != country2


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
    user1 = User(user_id=user_id, name="John Doe")

    user2 = User(user_id=user_id, name="John Doe Jr.")

    # Assert
    assert user1 == user2


def test_aggregates_with_different_id_are_not_equal():
    # Arrange
    user_id1 = UserID(101)
    user_id2 = UserID(102)

    # Act
    user1 = User(user_id=user_id1, name="John Doe")

    user2 = User(user_id=user_id2, name="John Doe")

    # Assert
    assert user1 != user2
