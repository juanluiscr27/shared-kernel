from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from sharedkernel.application.commands import Command
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
        return not self.errors

    @classmethod
    def success(cls):
        """Creates a ```ValidationResult``` with no errors """

        return cls()

    @classmethod
    def with_errors(cls, errors: List[Error]):
        """Creates a `ValidationResult` with the given list of errors

        Args:
            errors: Validation errors.
        """
        return cls(errors=errors)


class Validator(ABC):
    """Command Validator

    Perform input validation on the request
    """

    @abstractmethod
    def validate(self, command: Command) -> ValidationResult:
        """Validate that the command is processable.

        Args:
            command (Command): Command to validate.

        Returns:
            ValidationResult
        """
