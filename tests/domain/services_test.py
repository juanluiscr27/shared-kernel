from dataclasses import dataclass, field

import pytest

from sharedkernel.domain import ValueObject
from sharedkernel.domain.services import Guard


@dataclass(frozen=True)
class Email(ValueObject):
    value: str

    @classmethod
    def create(cls, value: str):
        Guard.is_not_null_or_empty(value)
        return cls(value)


@dataclass(frozen=True)
class MiddleName(ValueObject):
    value: str

    @classmethod
    def create(cls, value: str):
        Guard.is_not_null(value)
        return cls(value)


@dataclass(frozen=True)
class LastName(ValueObject):
    MAXIMUM_LENGTH: int = field(default=25, init=False)
    value: str

    @classmethod
    def create(cls, value: str):
        Guard.maximum_length(value, cls.MAXIMUM_LENGTH)
        return cls(value)


def test_object_with_empty_value_is_created():
    # Arrange
    middle_name_value = ""

    # Act
    result = MiddleName.create(middle_name_value)

    # Assert
    assert result.value == middle_name_value


def test_object_with_not_empty_or_null_value_is_created():
    # Arrange
    email_value = "example@email.com"

    # Act
    result = Email.create(email_value)

    # Assert
    assert result.value == email_value


def test_object_with_empty_value_raise_an_error():
    # Arrange
    empty_email = ""

    # Act
    with pytest.raises(ValueError) as error:
        _ = Email.create(empty_email)

    # Assert
    error_message = str(error.value)
    assert error_message == "Email cannot be null nor empty"


def test_object_with_null_value_raise_an_error():
    # Arrange
    null_email = None

    # Act
    with pytest.raises(ValueError) as error:
        # noinspection PyTypeChecker
        _ = Email.create(null_email)

    # Assert
    error_message = str(error.value)
    assert error_message == "Email cannot be null nor empty"


def test_object_with_appropriate_value_length_is_created():
    # Arrange
    last_name_value = "Smith"

    # Act
    result = LastName.create(last_name_value)

    # Assert
    assert result.value == last_name_value


def test_object_with_incorrect_value_length_raise_error():
    # Arrange
    last_name_value = "Diego José Francisco de Paula Juan Nepomuceno Cipriano de la Santísima Trinidad Ruiz Picasso"

    # Act
    with pytest.raises(ValueError) as error:
        _ = LastName.create(last_name_value)

    # Assert
    error_message = str(error.value)
    assert error_message == "LastName must be 25 characters or less"
