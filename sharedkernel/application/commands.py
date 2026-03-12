from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


@dataclass(frozen=True)
class Command:
    """Command base class

    A Command is an object that encapsulates a request into a stand-alone entity that contains all information about
    the request.
    """

    @property
    def qualname(self) -> str:
        """Returns the qualified name of the command class."""
        return self.__class__.__qualname__

    @property
    def full_qualname(self) -> str:
        """Returns the full qualified name of the command class (module + name)."""
        return f"{self.__module__}.{self.qualname}"


class CommandStatus(StrEnum):
    """Represents the execution status of a command."""
    RECEIVED = 'received'
    PROCESSING = 'processing'
    EXECUTED = 'executed'
    FAILED = 'failed'


@dataclass
class Acknowledgement:
    """Represents the acknowledgement of a command execution.

    Attributes:
        status: The execution status of the command.
        action: The name of the command that was executed.
        entity_id: The identifier of the entity affected by the command.
        version: The version number of the stream after the command execution.
    """
    status: CommandStatus
    action: str
    entity_id: UUID
    version: int


class CommandHandler[TCommand: Command](ABC):
    """Command Handler

    Is an object that orchestrates a business process and executes the activities that can be performed with the
    Domain Model. Command Handlers take `Commands` as input, validate it, and either accept or reject it.
    """

    @abstractmethod
    def execute(self, command: TCommand) -> Acknowledgement:
        """Execute a Command.

        Args:
            command: Command to execute.

        Returns:
            An acknowledgement of the command execution.

        Raises:
            DomainException: If a business rule is violated.
        """
