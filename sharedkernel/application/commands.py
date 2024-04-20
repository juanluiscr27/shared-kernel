from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from result import Result

from sharedkernel.domain.errors import Error


@dataclass(frozen=True)
class Command:
    """Command base class

    A Command is an object that encapsulates a request into a stand-alone entity that contains all information about
    the request.
    """


class CommandHandler(ABC):
    """Command Handler

    Is an object that orchestrates a business process and executes the activities that can be performed with the
    Domain Model. Command Handlers take `Commands` as input, validate it, and either accept or reject it.
    """

    @abstractmethod
    def execute(self, command: Command) -> Result[Any, Error]:
        """Execute a Command.

        Args:
            command: Command to execute.

        Returns:
            The execution result of the command. It could be success of type
            `Any` or an `Error`.
        """
