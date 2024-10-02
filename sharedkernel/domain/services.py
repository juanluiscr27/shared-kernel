import inspect
from typing import Optional, Any, TypeAlias


class DomainService:
    """Domain Service marker class.

    Encapsulates business logic that doesn't naturally fit within a domain object. A `DomainService` is specially
    useful when the logic needed to implement requires more than one aggregate. Additionally, when implementing a core
    domain logic that depends on some external services like repositories or external API.
    """


Number: TypeAlias = int | float


class Guard:
    """Guard is a class that implements strongly typed validation rules using
    guard clause technique. A guard clause is just a technique that promotes
    the "Failing Fast Principle" in a method, especially in a constructor.

    To work properly, the validation methods of this Guard class requires
    the caller to be a ``@classmethod`` that defines a `cls` variable which
     contains a reference to the caller class.
    """

    @staticmethod
    def _get_caller_name() -> str:
        """Implements object introspection to determine the caller qualified
        name.

        Returns:
            The caller class definition qualified name.

        Raises:
            KeyError: If the caller is not a class method with a `cls` variable
                that references its own class.
        """
        frame = inspect.currentframe()
        guard = frame.f_back
        caller = guard.f_back
        # If the caller method is not a class method with cls that reference
        # its own class will throw a 'KeyError'
        class_definition: type = caller.f_locals["cls"]
        return class_definition.__qualname__

    @staticmethod
    def is_not_null(value: Optional[str]) -> None:
        """Ensures that a specified value is not null.

        Args:
            value: Current value being validated.

        Raises:
            ValueError: If `value` is ``None``.
            KeyError: If the caller is not ``@classmethod`` with a `cls`
                variable that references its own class.
        """
        value_name = Guard._get_caller_name()

        if value is None:
            raise ValueError(f"{value_name} cannot be null")

    @staticmethod
    def is_not_empty(value: str) -> None:
        """Ensures that a specified property is not an empty string or
        whitespace.

        Args:
            value: Current value being validated.

        Raises:
            ValueError: If `value` is an empty string.
            KeyError: If the caller is not ``@classmethod`` with a `cls`
                variable that references its own class.
        """
        value_name = Guard._get_caller_name()

        if value.strip() == "":
            raise ValueError(f"{value_name} cannot be empty")

    @staticmethod
    def is_not_null_or_empty(value: Optional[str]) -> None:
        """Ensures that a specified value is not null, an empty string or
        whitespace.

        Args:
            value: Current value being validated.

        Raises:
            ValueError: If `value` is ``None`` or an empty string.
            KeyError: If the caller is not ``@classmethod`` with a `cls`
                variable that references its own class.
        """
        value_name = Guard._get_caller_name()

        if value is None or value.strip() == "":
            raise ValueError(f"{value_name} cannot be null nor empty")

    @staticmethod
    def is_null(value: Optional[str]) -> None:
        """Checks if a property value is null.

        It is the opposite of the ``is_not_null`` guard clause.

        Args:
            value: Current value being validated.

        Raises:
            ValueError: If `value` is not ``None``.
            KeyError: If the caller is not ``@classmethod`` with a `cls`
                variable that references its own class.
        """
        value_name = Guard._get_caller_name()

        if value is not None:
            raise ValueError(f"{value_name} must be null")

    @staticmethod
    def is_empty(value: str) -> None:
        """Checks if a property value is empty.

        It is the opposite of the ``is_not_empty`` guard clause.

        Args:
            value: Current value being validated.

        Raises:
            ValueError: If `value` is not an empty string.
            KeyError: If the caller is not ``@classmethod`` with a `cls`
                variable that references its own class.
        """
        value_name = Guard._get_caller_name()

        if value.strip() != "":
            raise ValueError(f"{value_name} must be empty")

    @staticmethod
    def is_equal(value: Any, reference_value: Any) -> None:
        """Ensures that a specified value is equal to a reference value.

        Args:
            value: Current value being validated.
            reference_value: Reference value to be compared.

        Raises:
            ValueError: If `value` is not equal to the `reference value`.
            KeyError: If the caller is not ``@classmethod`` with a `cls`
                variable that references its own class.
        """
        value_name = Guard._get_caller_name()

        if value != reference_value:
            raise ValueError(f"{value_name} should be equal to {reference_value}")

    @staticmethod
    def is_not_equal(value: Any, reference_value: Any) -> None:
        """Ensures that a specified value is not equal to a reference value.

        Args:
            value: Current value being validated.
            reference_value: Reference value to be compared.

        Raises:
            ValueError: If `value` is equal to the `reference value`.
            KeyError: If the caller is not ``@classmethod`` with a `cls`
                variable that references its own class.
        """
        value_name = Guard._get_caller_name()

        if value == reference_value:
            raise ValueError(f"{value_name} should not be equal to {reference_value}")

    @staticmethod
    def maximum_length(value: str, max_length: int) -> None:
        """Ensures that the length of a string value is no longer
         than a specified number of characters.

        Args:
            value: Current value being validated.
            max_length: Number that represents the maximum number of
                characters.

        Raises:
            ValueError: If the number of characters on `value` is greater than
                `max_length`.
            KeyError: If the caller is not ``@classmethod`` with a `cls`
                variable that references its own class.
        """
        value_name = Guard._get_caller_name()

        if len(value) > max_length:
            raise ValueError(f"{value_name} must be {max_length} characters or less")

    @staticmethod
    def minimum_length(value: str, min_length: int) -> None:
        """Ensures that the length of a string value is longer
        than a specified number of characters.

        Args:
            value: Current value being validated.
            min_length: Number that represents the minimum number of
                characters.

        Raises:
            ValueError: If the number of characters on `value` is lower than
                `max_length`.
            KeyError: If the caller is not ``@classmethod`` with a `cls`
                variable that references its own class.
        """
        value_name = Guard._get_caller_name()

        if len(value) < min_length:
            raise ValueError(f"{value_name} must be {min_length} characters or more")

    @staticmethod
    def is_less_than(value: Number, reference_value: Number) -> None:
        """Ensures that a numeric value is less than a reference value.

        Raises:
            ValueError: If `value` is not less than `reference_value`.
            KeyError: If the caller is not ``@classmethod`` with a `cls`
                variable that references its own class.
        """
        value_name = Guard._get_caller_name()

        if not value < reference_value:
            raise ValueError(f"{value_name} must be less than {reference_value}")

    @staticmethod
    def is_less_than_or_equal(value: Number, reference_value: Number) -> None:
        """Ensures that a numeric value is less than or equal a reference
        value.

        Args:
            value: Current value being validated.
            reference_value: Reference value to be compared.

        Raises:
            ValueError: If `value` is greater than `reference_value`.
            KeyError: If the caller is not ``@classmethod`` with a `cls`
                variable that references its own class.
        """
        value_name = Guard._get_caller_name()

        if value > reference_value:
            raise ValueError(f"{value_name} must be less than or equal to {reference_value}")

    @staticmethod
    def is_greater_than(value: Number, reference_value: Number) -> None:
        """Ensures that a numeric value is greater than a reference value.

        Args:
            value: Current value being validated.
            reference_value: Reference value to be compared.

        Raises:
            ValueError: If `value` is not greater than `reference_value`.
            KeyError: If the caller is not ``@classmethod`` with a `cls`
                variable that references its own class.
        """
        value_name = Guard._get_caller_name()

        if not value > reference_value:
            raise ValueError(f"{value_name} must be greater than {reference_value}")

    @staticmethod
    def is_greater_than_or_equal(value: Number, reference_value: Number) -> None:
        """Ensures that a numeric value is greater than or equal a reference
        value.

        Args:
            value: Current value being validated.
            reference_value: Reference value to be compared.

        Raises:
            ValueError: If `value` is less than `reference_value`.
            KeyError: If the caller is not ``@classmethod`` with a `cls`
                variable that references its own class.
        """
        value_name = Guard._get_caller_name()

        if value < reference_value:
            raise ValueError(f"{value_name} must be greater than or equal to {reference_value}")


class Detect:
    """Detect is a class that provides methods to check text input to prevent
    SQL injection attacks.

    Detect can identify special characters and reserved words of the SQL syntax.
    """

    @staticmethod
    def special_character(text: str) -> None:
        """Checks that a given text has SQL special characters.

        Args:
            text: Text input being validated.

        Raises:
            ValueError: If `text` contains a SQL special character.
        """
        if '"' in text:
            raise ValueError("Text contains an invalid character")

        if "<" in text:
            raise ValueError("Text contains an invalid character")

        if ">" in text:
            raise ValueError("Text contains an invalid character")

        if ";" in text:
            raise ValueError("Text contains an invalid character")

        if "#" in text:
            raise ValueError("Text contains an invalid character")

        if "$" in text:
            raise ValueError("Text contains an invalid character")

        if "%" in text:
            raise ValueError("Text contains an invalid character")

        if "^" in text:
            raise ValueError("Text contains an invalid character")

        if "&" in text:
            raise ValueError("Text contains an invalid character")

        if "*" in text:
            raise ValueError("Text contains an invalid character")

        if "(" in text:
            raise ValueError("Text contains an invalid character")

        if ")" in text:
            raise ValueError("Text contains an invalid character")

        if "=" in text:
            raise ValueError("Text contains an invalid character")

        if "@@" in text:
            raise ValueError("Text contains an invalid character")

        if "||" in text:
            raise ValueError("Text contains an invalid character")

        if "--" in text:
            raise ValueError("Text contains an invalid character")

    @staticmethod
    def reserved_word(text: str) -> None:
        """Checks that a given text has SQL reserved words.

        Args:
            text: Text input being validated.

        Raises:
            ValueError: If `text` contains SQL reserved word.
        """

        if "ALTER " in text.upper():
            raise ValueError("Text contains an invalid word")

        if "CREATE " in text.upper():
            raise ValueError("Text contains an invalid word")

        if "DELETE " in text.upper():
            raise ValueError("Text contains an invalid word")

        if "DROP " in text.upper():
            raise ValueError("Text contains an invalid word")

        if "EXECUTE " in text.upper():
            raise ValueError("Text contains an invalid word")

        if "INSERT " in text.upper():
            raise ValueError("Text contains an invalid word")

        if "MERGE " in text.upper():
            raise ValueError("Text contains an invalid word")

        if "SELECT " in text.upper():
            raise ValueError("Text contains an invalid word")

        if "UPDATE " in text.upper():
            raise ValueError("Text contains an invalid word")

        if " OR " in text.upper():
            raise ValueError("Text contains an invalid word")

        if " TABLE " in text.upper():
            raise ValueError("Text contains an invalid word")
