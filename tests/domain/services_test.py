from dataclasses import dataclass, field
from typing import Any

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
        Guard.is_not_equal(value.lower(), "root")
        Detect.special_character(value)
        Detect.reserved_word(value)
        return cls(value)


@dataclass(frozen=True)
class Password(ValueObject):
    MAXIMUM_LENGTH: int = field(default=12, init=False)
    MINIMUM_LENGTH: int = field(default=8, init=False)
    value: str

    @classmethod
    def create(cls, value: str):
        Guard.is_not_null(value)
        Guard.maximum_length(value, cls.MAXIMUM_LENGTH)
        Guard.minimum_length(value, cls.MINIMUM_LENGTH)
        return cls(value)


@dataclass(frozen=True)
class Comment(ValueObject):
    value: str

    @classmethod
    def create(cls, value: str):
        Guard.is_not_empty(value)
        return cls(value)


@dataclass(frozen=True)
class LastUpdated(ValueObject):
    value: Any

    @classmethod
    def create(cls, value: Any):
        Guard.is_null(value)
        return cls(value)


@dataclass(frozen=True)
class Directory(ValueObject):
    value: str

    @classmethod
    def create(cls, value: str):
        Guard.is_empty(value)
        return cls(value)


@dataclass(frozen=True)
class CountryID(ValueObject):
    SIZE: int = field(default=2, init=False)
    value: str

    @classmethod
    def create(cls, value: str):
        Guard.is_equal(len(value), cls.SIZE)
        return cls(value)


@dataclass(frozen=True)
class Capacity(ValueObject):
    MAXIMUM: int = field(default=1000, init=False)
    value: int

    @classmethod
    def create(cls, value: int):
        Guard.is_greater_than(value, 0)
        Guard.is_less_than(value, cls.MAXIMUM)
        return cls(value)


@dataclass(frozen=True)
class Amount(ValueObject):
    MAXIMUM: int = field(default=100, init=False)
    years: float

    @classmethod
    def create(cls, value: float):
        Guard.is_greater_than(value, 0)
        Guard.is_less_than_or_equal(value, cls.MAXIMUM)
        return cls(value)


def test_object_with_not_null_value_is_created():
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


def test_object_with_null_value_is_created():
    # Arrange
    null_date = None

    # Act
    result = LastUpdated.create(null_date)

    # Assert
    assert result.value is None


def test_object_with_not_null_value_raise_an_error():
    # Arrange
    null_date = "2024-10-31T01:30:00.000-04:00"

    # Act
    with pytest.raises(ValueError) as error:
        _ = LastUpdated.create(null_date)

    error_message = str(error.value)

    # Assert
    assert error_message == "LastUpdated must be null"


def test_object_with_empty_value_is_created():
    # Arrange
    path = ""

    # Act
    result = Directory.create(path)

    # Assert
    assert result.value == ""


def test_object_with_not_empty_value_raise_an_error():
    # Arrange
    path = "/usr/local/lib/python3"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Directory.create(path)

    error_message = str(error.value)

    # Assert
    assert error_message == "Directory must be empty"


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


def test_object_with_reserved_name_raise_an_error():
    # Arrange
    user = "root"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(user)

    error_message = str(error.value)

    # Assert
    assert error_message == "Username should not be equal to root"


def test_text_with_equal_sign_raise_an_error():
    # Arrange
    special_text = "1 = 1"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_quotes_raise_an_error():
    # Arrange
    special_text = '"USERS"'

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_less_than_sign_raise_an_error():
    # Arrange
    special_text = "0 < 1"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_greater_than_sign_raise_an_error():
    # Arrange
    special_text = "1 > 0"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_semi_colon_raise_an_error():
    # Arrange
    special_text = "TRUE;"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_number_sign_raise_an_error():
    # Arrange
    special_text = "#TempTables"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_money_sign_raise_an_error():
    # Arrange
    special_text = "AS $$ DECLARE"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_percentage_sign_raise_an_error():
    # Arrange
    special_text = "%admin%"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_caret_sign_raise_an_error():
    # Arrange
    special_text = "5 ^ 3"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_ampersand_sign_raise_an_error():
    # Arrange
    special_text = "&user"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_asterisk_sign_raise_an_error():
    # Arrange
    special_text = "*"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_open_parenthesis_raise_an_error():
    # Arrange
    special_text = "(user"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_close_parenthesis_raise_an_error():
    # Arrange
    special_text = "user)"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_system_variable_raise_an_error():
    # Arrange
    special_text = "@@CHARACTER_SET_CLIENT"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_concat_operator_raise_an_error():
    # Arrange
    special_text = ":name || :password"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_comment_sign_raise_an_error():
    # Arrange
    special_text = "true --"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid character"


def test_text_with_drop_reserved_word_raise_an_error():
    # Arrange
    special_text = "DROP TABLE users"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Username.create(special_text)

    error_message = str(error.value)

    # Assert
    assert error_message == "Text contains an invalid word"


def test_object_with_valid_length_is_created():
    # Arrange
    password = "Admin123"

    # Act
    result = Password.create(password)

    # Assert
    assert result.value == "Admin123"


def test_object_with_short_value_raise_an_error():
    # Arrange
    password = "12345"

    # Act
    with pytest.raises(ValueError) as error:
        _ = Password.create(password)

    error_message = str(error.value)

    # Assert
    assert error_message == "Password must be 8 characters or more"


def test_object_with_equal_value_is_created():
    # Arrange
    usa = "US"

    # Act
    result = CountryID.create(usa)

    # Assert
    assert result.value == "US"


def test_object_with_not_equal_value_raise_an_error():
    # Arrange
    usa = "USA"

    # Act
    with pytest.raises(ValueError) as error:
        _ = CountryID.create(usa)

    error_message = str(error.value)

    # Assert
    assert error_message == "CountryID should be equal to 2"


def test_object_with_lower_value_is_created():
    # Arrange
    total = 500

    # Act
    result = Capacity.create(total)

    # Assert
    assert result.value == 500


def test_object_with_not_lower_value_raise_an_error():
    # Arrange
    total = 1500

    # Act
    with pytest.raises(ValueError) as error:
        _ = Capacity.create(total)

    error_message = str(error.value)

    # Assert
    assert error_message == "Capacity must be less than 1000"


def test_object_with_value_within_limits_is_created():
    # Arrange
    fifty = 50

    # Act
    result = Amount.create(fifty)

    # Assert
    assert result.years == 50


def test_object_with_value_less_raise_error():
    # Arrange
    negative_quantity = -3

    # Act
    with pytest.raises(ValueError) as error:
        _ = Amount.create(negative_quantity)

    error_message = str(error.value)

    # Assert
    assert error_message == "Amount must be greater than 0"


def test_object_with_value_greater_raise_error():
    # Arrange
    value_over = 110

    # Act
    with pytest.raises(ValueError) as error:
        _ = Amount.create(value_over)

    error_message = str(error.value)

    # Assert
    assert error_message == "Amount must be less than or equal to 100"
