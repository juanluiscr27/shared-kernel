from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import TypeVar, Generic
from uuid import UUID

from result import Result

from sharedkernel.domain.errors import Error


@dataclass(frozen=True)
class Command:
    """Command base class

    A Command is an object that encapsulates a request into a stand-alone entity that contains all information about
    the request.
    """


class CommandStatus(StrEnum):
    RECEIVED = 'received'
    PROCESSING = 'processing'
    EXECUTED = 'executed'
    FAILED = 'failed'


@dataclass
class Acknowledgement:
    status: CommandStatus
    action: str
    entity_id: UUID
    version: int


TCommand = TypeVar("TCommand", bound=Command)


class CommandHandler(ABC, Generic[TCommand]):
    """Command Handler

    Is an object that orchestrates a business process and executes the activities that can be performed with the
    Domain Model. Command Handlers take `Commands` as input, validate it, and either accept or reject it.
    """

    @abstractmethod
    def execute(self, command: TCommand) -> Result[Acknowledgement, Error]:
        """Execute a Command.

        Args:
            command: Command to execute.

        Returns:
            The execution result of the command.
            It could be an acknowledgement of success or an `Error`.
        """
