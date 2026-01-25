from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, TypeVar, Generic

from sharedkernel.application.commands import Command
from sharedkernel.application.queries import Query
from sharedkernel.domain.errors import Error


@dataclass(frozen=True)
class ValidationResult:
    """Validation Result class

    Instances of `ValidationResult` should be created using the ```success```
    or ```with_errors``` functions.
    """
    errors: List[Error] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Indicates if the validation result contains any errors."""
        return not self.errors

    @classmethod
    def success(cls):
        """Creates a ValidationResult with no errors."""

        return cls()

    @classmethod
    def with_errors(cls, errors: List[Error]):
        """Creates a ValidationResult with a given list of errors.

        Args:
            errors: A list of validation errors.
        """
        return cls(errors=errors)


TRequest = TypeVar("TRequest", bound=Command | Query)


class Validator(ABC, Generic[TRequest]):
    """Validator for Command or Query

    Perform input validation on the request
    """

    @abstractmethod
    def validate(self, request: TRequest) -> ValidationResult:
        """Validate that the request is processable.

        Args:
            request: Command or Query to validate.

        Returns:
            ValidationResult
        """
