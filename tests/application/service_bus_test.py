from dataclasses import dataclass
from uuid import UUID

import pytest
from result import Result, Ok, Err

from sharedkernel.application.commands import Command, CommandHandler, Acknowledgement, CommandStatus
from sharedkernel.application.errors import UnsupportedHandler
from sharedkernel.application.queries import Query, QueryHandler
from sharedkernel.application.services import ServiceBus
from sharedkernel.application.validators import Validator, ValidationResult
from sharedkernel.domain.data import ReadModel
from sharedkernel.domain.errors import Error
from sharedkernel.domain.events import DomainEvent, DomainEventHandler


@dataclass(frozen=True)
class UserModel(ReadModel):
    user_id: UUID
    name: str
    slug: str


@dataclass(frozen=True)
class RegisterUser(Command):
    user_id: UUID
    name: str
    slug: str


@dataclass(frozen=True)
class GetUserByID(Query):
    user_id: UUID


def name_null_or_empty_error() -> Error:
    return Error(
        message="User name is null or empty.",
        code="User.Name.NullOrEmpty",
        reason=f"User 'name' should not be null nor empty.",
        domain="Test.Users.RegisterUser",
    )


def slug_not_unique_error(slug: str) -> Error:
    return Error(
        message="User slug is not unique.",
        code="User.Slug.NotUnique",
        reason=f"User slug '{slug}' already exists.",
        domain="Test.Users.RegisterUser",
    )


def id_not_found(user_id: str) -> Error:
    return Error(
        message=f"User id '{user_id} not found'.",
        code="User.Id.NotFound",
        reason=f"User 'ID' is not available.",
        domain="Test.users.GetUserById",
    )


class RegisterUserCommandHandler(CommandHandler[RegisterUser]):

    def execute(self, command: RegisterUser) -> Result[Acknowledgement, Error]:
        if command.user_id == UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'):
            ack = Acknowledgement(
                status=CommandStatus.RECEIVED,
                action="RegisterUser",
                entity_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
                position=1, )
            return Ok(ack)
        else:
            error = slug_not_unique_error(command.slug)
            return Err(error)


class GetUserByIDQueryHandler(QueryHandler[GetUserByID]):

    def execute(self, command: GetUserByID) -> Result[ReadModel, Error]:
        if command.user_id == UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'):
            user = UserModel(
                user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
                name="John Doe Smith",
                slug="john-doe-smith",
            )
            return Ok(user)
        else:
            error = id_not_found(str(command.user_id))
            return Err(error)


class RegisterOfficialValidator(Validator[RegisterUser]):

    def validate(self, request: RegisterUser) -> ValidationResult:
        errors = []

        if request.name is None or request.name.strip() == "":
            name_null_or_empty = name_null_or_empty_error()
            errors.append(name_null_or_empty)
        if errors:
            return ValidationResult.with_errors(errors=errors)
        else:
            return ValidationResult.success()


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    event_id: str
    message: str


class RegistrationEventHandler(DomainEventHandler[UserRegistered]):

    def process(self, event: UserRegistered):
        pass


def test_command_handler_is_registered_to_service_bus(fake_logger):
    # Arrange
    bus = ServiceBus(fake_logger)
    handler = RegisterUserCommandHandler()

    # Act
    result = bus.register(handler)

    # Assert
    assert result is True


def test_query_handler_is_registered_to_service_bus(fake_logger):
    # Arrange
    bus = ServiceBus(fake_logger)
    validator = RegisterOfficialValidator()

    # Act
    result = bus.register(validator)

    # Assert
    assert result is True


def test_validator_is_registered_to_service_bus(fake_logger):
    # Arrange
    bus = ServiceBus(fake_logger)
    handler = GetUserByIDQueryHandler()

    # Act
    result = bus.register(handler)

    # Assert
    assert result is True


def test_registering_event_handler_service_bus_raise_error(fake_logger):
    # Arrange
    expected = "`RegistrationEventHandler` cannot be registered to ServiceBus"

    bus = ServiceBus(fake_logger)
    handler = RegistrationEventHandler()

    # Act
    with pytest.raises(UnsupportedHandler) as error:
        # noinspection PyTypeChecker
        _ = bus.register(handler)

    # Assert
    assert str(error.value) == expected


def test_pre_process_request_with_no_validator_return_valid_result(fake_logger):
    # Arrange
    bus = ServiceBus(fake_logger)
    command = RegisterUser(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    # Act
    result = bus.pre_process(command)

    # Assert
    assert result.is_valid is True


def test_pre_process_valid_request_return_valid_result(fake_logger):
    # Arrange
    bus = ServiceBus(fake_logger)
    validator = RegisterOfficialValidator()
    bus.register(validator)

    command = RegisterUser(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    # Act
    result = bus.pre_process(command)

    # Assert
    assert result.is_valid is True


def test_pre_process_invalid_request_return_validation_errors(fake_logger):
    # Arrange
    bus = ServiceBus(fake_logger)
    validator = RegisterOfficialValidator()
    bus.register(validator)

    command = RegisterUser(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        name="",
        slug="john-doe-smith",
    )

    # Act
    result = bus.pre_process(command)

    # Assert
    assert result.is_valid is False


def test_process_command_with_handler_return_rejection(fake_logger):
    # Arrange
    expected = 501
    bus = ServiceBus(fake_logger)

    command = RegisterUser(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    # Act
    result = bus.process_command(command)

    # Assert
    assert result.status_code == expected


def test_process_valid_command_return_command_acknowledgment(fake_logger):
    # Arrange
    bus = ServiceBus(fake_logger)
    handler = RegisterUserCommandHandler()
    bus.register(handler)

    command = RegisterUser(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    # Act
    result = bus.process_command(command)

    # Assert
    assert result.status is CommandStatus.RECEIVED


def test_process_invalid_command_return_rejection(fake_logger):
    # Arrange
    expected = 422
    bus = ServiceBus(fake_logger)
    handler = RegisterUserCommandHandler()
    bus.register(handler)

    command = RegisterUser(
        user_id=UUID('018f928b-5546-77e6-badf-3155de144924'),
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    # Act
    result = bus.process_command(command)

    # Assert
    assert result.status_code == expected


def test_process_query_with_handler_return_rejection(fake_logger):
    # Arrange
    expected = 501
    user_id = UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c')

    bus = ServiceBus(fake_logger)

    query = GetUserByID(user_id=user_id)

    # Act
    result = bus.process_query(query)

    # Assert
    assert result.status_code == expected


def test_process_valid_query_return_read_model(fake_logger):
    # Arrange
    user_id = UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c')

    bus = ServiceBus(fake_logger)
    handler = GetUserByIDQueryHandler()
    bus.register(handler)

    query = GetUserByID(user_id=user_id)

    # Act
    result = bus.process_query(query)

    # Assert
    assert result.user_id == user_id


def test_process_invalid_query_return_rejection(fake_logger):
    # Arrange
    user_id = UUID('018f928b-5546-77e6-badf-3155de144924')

    expected = 404
    bus = ServiceBus(fake_logger)
    handler = GetUserByIDQueryHandler()
    bus.register(handler)

    query = GetUserByID(user_id=user_id)

    # Act
    result = bus.process_query(query)

    # Assert
    assert result.status_code == expected


def test_send_valid_command_return_command_acknowledgment(fake_logger):
    # Arrange
    bus = ServiceBus(fake_logger)
    handler = RegisterUserCommandHandler()
    bus.register(handler)

    command = RegisterUser(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    # Act
    result = bus.send(command)

    # Assert
    assert result.status is CommandStatus.RECEIVED


def test_send_valid_query_return_read_model(fake_logger):
    # Arrange
    user_id = UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c')

    bus = ServiceBus(fake_logger)
    handler = GetUserByIDQueryHandler()
    bus.register(handler)

    query = GetUserByID(user_id=user_id)

    # Act
    result = bus.send(query)

    # Assert
    assert result.user_id == user_id
