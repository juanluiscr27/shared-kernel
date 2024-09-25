from dataclasses import dataclass, field

import pytest

from sharedkernel.domain.models import ValueObject
from sharedkernel.domain.services import Guard, Detect


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


@dataclass(frozen=True)
class Age(ValueObject):
    MAXIMUM_AGE: int = field(default=120, init=False)
    years: float

    @classmethod
    def create(cls, value: float):
        Guard.is_greater_than_or_equal(value, 0)
        Guard.is_less_than(value, cls.MAXIMUM_AGE)
        return cls(value)


@dataclass(frozen=True)
class Username(ValueObject):
    value: str

    @classmethod
    def create(cls, value: str):
        Guard.is_not_null(value)
        Detect.special_character(value)
        Detect.reserved_word(value)
        return cls(value)


@dataclass(frozen=True)
class Comment(ValueObject):
    value: str

    @classmethod
    def create(cls, value: str):
        Guard.is_not_empty(value)
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


def test_object_with_not_null_but_empty_value_raise_an_error():
    # Arrange
    empty_email = ""

    # Act
    with pytest.raises(ValueError) as error:
        _ = Email.create(empty_email)

    error_message = str(error.value)

    # Assert
    assert error_message == "Email cannot be null nor empty"


def test_object_with_null_value_but_not_empty_raise_an_error():
    # Arrange
    null_email = None

    # Act
    with pytest.raises(ValueError) as error:
        # noinspection PyTypeChecker
        _ = Email.create(null_email)

    error_message = str(error.value)

    # Assert
    assert error_message == "Email cannot be null nor empty"


def test_object_with_null_value_raise_an_error():
    # Arrange
    null_username = None

    # Act
    with pytest.raises(ValueError) as error:
        # noinspection PyTypeChecker
        _ = Username.create(null_username)

    error_message = str(error.value)

    # Assert
    assert error_message == "Username cannot be null"


def test_object_with_empty_value_raise_an_error():
    # Arrange
    comment = ""

    # Act
    with pytest.raises(ValueError) as error:
        _ = Comment.create(comment)

    error_message = str(error.value)

    # Assert
    assert error_message == "Comment cannot be empty"


def test_object_with_not_empty_value_is_created():
    # Arrange
    comment = "Great content!"

    # Act
    result = Comment.create(comment)

    # Assert
    assert result.value == comment


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

    error_message = str(error.value)

    # Assert
    assert error_message == "LastName must be 25 characters or less"


def test_object_with_value_within_range_is_created():
    # Arrange
    twenty_five = 25

    # Act
    result = Age.create(twenty_five)

    # Assert
    assert result.years == twenty_five


def test_object_with_value_under_range_raise_error():
    # Arrange
    negative_age = -3

    # Act
    with pytest.raises(ValueError) as error:
        _ = Age.create(negative_age)

    error_message = str(error.value)

    # Assert
    assert error_message == "Age must be greater than or equal to 0"


def test_object_with_value_over_range_raise_error():
    # Arrange
    two_hundreds = 200

    # Act
    with pytest.raises(ValueError) as error:
        _ = Age.create(two_hundreds)

    error_message = str(error.value)

    # Assert
    assert error_message == "Age must be less than 120"


def test_object_with_sanitized_text_is_created():
    # Arrange
    username_value = "johndoe"

    # Act
    result = Username.create(username_value)

    # Assert
    assert result.value == username_value


def test_object_with_special_character_raise_an_error():
    # Arrange
    special_text = "1 = 1"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Username contains an invalid character"


def test_object_with_reserved_word_raise_an_error():
    # Arrange
    special_text = "DROP TABLE users"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Username contains an invalid word"
