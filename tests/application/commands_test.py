from dataclasses import dataclass

from sharedkernel.application.commands import Command


@dataclass(frozen=True)
class RegisterUser(Command):
    name: str


def test_command_qualname():
    # Arrange
    expected = "RegisterUser"

    # Act
    command = RegisterUser(name="John Doe")

    # Assert
    assert command.qualname == expected


def test_command_full_qualname():
    # Arrange
    expected = "tests.application.commands_test.RegisterUser"

    # Act
    command = RegisterUser(name="John Doe")

    # Assert
    assert command.full_qualname == expected
