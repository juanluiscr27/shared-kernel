from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

import pytest

from sharedkernel.application.commands import Acknowledgement, Command, CommandHandler, CommandStatus
from sharedkernel.application.errors import HandlerAlreadyRegistered, UnsupportedHandler
from sharedkernel.application.queries import Query, QueryHandler
from sharedkernel.application.services import RequestContext, ServiceBus, get_request_id
from sharedkernel.application.validators import ValidationResult, Validator
from sharedkernel.domain.data import ReadModel, ReadModelList
from sharedkernel.domain.errors import EntityNotFound, Error, UniqueConstraintViolation
from sharedkernel.domain.events import DomainEvent, DomainEventHandler


class DuplicateName(UniqueConstraintViolation):
    def __init__(self, source: object, name: str):
        message = f"User '{name}' has already been selected."
        super().__init__(source=source, message=message)


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


@dataclass(frozen=True)
class GetAllUsers(Query):
    pass


def name_null_or_empty_error() -> Error:
    return Error(
        message="User name is null or empty.",
        code="User.Name.NullOrEmpty",
        reason="User 'name' should not be null nor empty.",
        domain="Test.Users.RegisterUser",
    )


class SlugNotUnique(UniqueConstraintViolation):
    def __init__(self, source: object, slug: str):
        message = f"User slug '{slug}' is not unique."
        super().__init__(source=source, message=message)


class UserNotFound(EntityNotFound):
    def __init__(self, source: object, user_id: str):
        message = f"User id '{user_id}' not found."
        super().__init__(source=source, message=message)


class RegisterUserCommandHandler(CommandHandler[RegisterUser]):

    def execute(self, command: RegisterUser) -> Acknowledgement:
        if command.name == "John Doe":
            raise DuplicateName(self, command.name)

        if command.user_id == UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'):
            return Acknowledgement(
                status=CommandStatus.RECEIVED,
                action="RegisterUser",
                entity_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
                version=1,
            )
        raise SlugNotUnique(self, command.slug)


class GetUserByIDQueryHandler(QueryHandler[GetUserByID]):

    def execute(self, query: GetUserByID) -> ReadModel:
        if query.user_id == UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'):
            return UserModel(
                user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
                name="John Doe Smith",
                slug="john-doe-smith",
            )
        raise UserNotFound(self, str(query.user_id))


class GetAllUsersQueryHandler(QueryHandler[GetAllUsers]):

    def execute(self, query: GetAllUsers) -> ReadModelList:
        all_user = [UserModel(
            user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
            name="John Doe Smith",
            slug="john-doe-smith",
        )]

        return ReadModelList(
            offset=0,
            limit=1,
            total=1,
            items=all_user,
        )


class RegisterOfficialValidator(Validator[RegisterUser]):

    def validate(self, request: RegisterUser) -> ValidationResult:
        errors = []

        if request.name is None or request.name.strip() == "":
            name_null_or_empty = name_null_or_empty_error()
            errors.append(name_null_or_empty)
        if errors:
            return ValidationResult.with_errors(errors=errors)
        return ValidationResult.success()


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    event_id: str
    message: str


class RegistrationEventHandler(DomainEventHandler[UserRegistered]):

    def process(self, event: UserRegistered, position: int):
        pass


class RegisterUserWithContextHandler(CommandHandler[RegisterUser]):

    def execute(self, command: RegisterUser) -> Acknowledgement:
        if command.name == "John Doe":
            raise DuplicateName(self, command.name)

        if command.user_id == UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'):
            print(f"{type(command).__name__}(request_id={get_request_id()})")
            return Acknowledgement(
                status=CommandStatus.RECEIVED,
                action="RegisterUser",
                entity_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
                version=1,
            )
        raise SlugNotUnique(self, command.slug)


class FaultyRegisterUserHandler(CommandHandler[RegisterUser]):

    def execute(self, command: RegisterUser) -> Acknowledgement:
        raise ValueError('User data format is invalid.')


@pytest.fixture
def fake_context():
    timestamp = datetime.fromisoformat('2026-01-24T14:45:15-04:00')
    request_id = UUID('019bf1bf-7398-7860-b4a8-9cafdda482ff')

    return RequestContext.new(
        request_id=request_id,
        timestamp=timestamp,
    )


def test_command_handler_is_registered_to_service_bus(fake_logger):
    # Arrange
    bus = ServiceBus(fake_logger)
    handler = RegisterUserCommandHandler()

    # Act
    result = bus.register(handler)

    # Assert
    assert result is True


def test_register_command_handler_twice_raise_error(fake_logger):
    # Arrange
    bus = ServiceBus(fake_logger)
    handler = RegisterUserCommandHandler()

    expected = "A Handler has been already registered for `RegisterUser`"

    # Act
    bus.register(handler)

    with pytest.raises(HandlerAlreadyRegistered) as error:
        # noinspection PyTypeChecker
        _ = bus.register(handler)

    # Assert
    assert str(error.value) == expected


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
    bus = ServiceBus(fake_logger)
    handler = RegistrationEventHandler()

    expected = "`RegistrationEventHandler` cannot be registered to ServiceBus"

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


def test_process_command_with_no_handler_return_rejection(fake_logger):
    # Arrange
    bus = ServiceBus(fake_logger)

    command = RegisterUser(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    expected = 501

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


def test_process_invalid_command_raises_exception(fake_logger):
    # Arrange
    bus = ServiceBus(fake_logger)
    handler = RegisterUserCommandHandler()
    bus.register(handler)

    command = RegisterUser(
        user_id=UUID('018f928b-5546-77e6-badf-3155de144924'),
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    # Act & Assert
    with pytest.raises(UniqueConstraintViolation):
        bus.process_command(command)


def test_process_query_with_handler_return_rejection(fake_logger):
    # Arrange
    user_id = UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c')

    bus = ServiceBus(fake_logger)

    query = GetUserByID(user_id=user_id)

    expected = 501

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


def test_process_invalid_query_raises_exception(fake_logger):
    # Arrange
    user_id = UUID('018f928b-5546-77e6-badf-3155de144924')

    bus = ServiceBus(fake_logger)
    handler = GetUserByIDQueryHandler()
    bus.register(handler)

    query = GetUserByID(user_id=user_id)

    # Act & Assert
    with pytest.raises(EntityNotFound):
        bus.process_query(query)


def test_send_valid_command_return_command_acknowledgment(fake_logger, fake_context):
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
    result = bus.send(command, fake_context)

    # Assert
    assert result.status is CommandStatus.RECEIVED


def test_send_valid_query_return_read_model(fake_logger, fake_context):
    # Arrange
    user_id = UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c')

    bus = ServiceBus(fake_logger)
    handler = GetUserByIDQueryHandler()
    bus.register(handler)

    query = GetUserByID(user_id=user_id)

    # Act
    result = bus.send(query, fake_context)

    # Assert
    assert result.user_id == user_id


def test_send_valid_query_return_read_model_list(fake_logger, fake_context):
    # Arrange
    bus = ServiceBus(fake_logger)
    handler = GetAllUsersQueryHandler()
    bus.register(handler)

    query = GetAllUsers()

    # Act
    result = bus.send(query, fake_context)

    # Assert
    assert result.total == 1


def test_send_event_as_request_return_rejection(fake_logger, fake_context):
    # Arrange
    user_registered = UserRegistered(
        event_id='01921c1b-18b9-7d74-ac5e-4a4c7570dca7',
        message='UserRegistered',
    )

    bus = ServiceBus(fake_logger)

    # Act
    # noinspection PyTypeChecker
    result = bus.send(user_registered, fake_context)

    # Assert
    assert len(result.errors) == 1


def test_send_invalid_request_return_rejection(fake_logger, fake_context):
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
    result = bus.send(command, fake_context)

    # Assert
    assert len(result.errors) == 1


def test_send_conflicting_command_return_rejection(fake_logger, fake_context):
    # Arrange
    bus = ServiceBus(fake_logger)
    handler = RegisterUserCommandHandler()
    bus.register(handler)

    command = RegisterUser(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        name="John Doe",
        slug="john-doe-smith",
    )

    # Act
    result = bus.send(command, fake_context)

    # Assert
    assert len(result.errors) == 1


def test_send_valid_command_with_context_set_request_id(fake_logger, fake_context, capture_stdout):
    # Arrange
    bus = ServiceBus(fake_logger)
    handler = RegisterUserWithContextHandler()
    bus.register(handler)
    console = "RegisterUser(request_id=019bf1bf-7398-7860-b4a8-9cafdda482ff)\n"

    command = RegisterUser(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    # Act
    _ = bus.send(command, fake_context)

    # Assert
    assert capture_stdout["console"] == console


def test_send_valid_command_with_context_reset_request_id(fake_logger, fake_context):
    # Arrange
    bus = ServiceBus(fake_logger)
    handler = RegisterUserWithContextHandler()
    bus.register(handler)

    command = RegisterUser(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    # Act
    _ = bus.send(command, fake_context)
    result = get_request_id()

    # Assert
    assert result != fake_context.request_id


def test_send_command_to_faulty_handler_raises_error(fake_logger, fake_context):
    # Arrange
    bus = ServiceBus(fake_logger)
    handler = FaultyRegisterUserHandler()
    bus.register(handler)

    command = RegisterUser(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    # Act
    with pytest.raises(ValueError) as error:
        _ = bus.send(command, fake_context)

    error_message = str(error.value)

    # Assert
    assert error_message == "User data format is invalid."


def test_new_request_context_with_no_datetime_param_set_datetime_now():
    # Arrange
    request_id = UUID('019bf1bf-7398-7860-b4a8-9cafdda482ff')

    # Act
    result = RequestContext.new(request_id=request_id)

    # Assert
    assert result.timestamp is not None
