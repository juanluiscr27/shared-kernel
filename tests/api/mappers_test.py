from dataclasses import dataclass
from typing import Optional
from uuid import UUID

import pytest

from sharedkernel.api.contracts import Request
from sharedkernel.api.errors import RequestMapperNotFound
from sharedkernel.api.mappers import RequestMapper
from sharedkernel.api.mappers import RequestMappersChain
from sharedkernel.application.commands import Command


class RegisterUserRequest(Request):
    user_id: str
    name: str
    slug: str


class LogInUserRequest(Request):
    name: str
    email: str


@dataclass(frozen=True)
class RegisterUser(Command):
    user_id: UUID
    name: str
    slug: str


class RegisterUserRequestMapper(RequestMapper[RegisterUserRequest]):

    def map(self, request: RegisterUserRequest, **query_params) -> Optional[RegisterUser]:
        if type(request).__name__ != self.request_type:
            return self.map_next(request, **query_params)

        return RegisterUser(
            user_id=UUID(request.user_id),
            name=request.name,
            slug=request.slug,
        )


def test_mapper_return_command_event_with_valid_request():
    # Arrange
    expected = RegisterUser(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    request = RegisterUserRequest(
        user_id='018f9284-769b-726d-b3bf-3885bf2ddd3c',
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    mapper = RegisterUserRequestMapper()

    # Act
    result = mapper.map(request)

    # Assert
    assert result == expected


def test_mapper_return_none_with_unknown_request():
    # Arrange
    request = LogInUserRequest(
        name="John Doe",
        email="john-doe@example.com",
    )

    mapper = RegisterUserRequestMapper()

    # Act
    # noinspection PyTypeChecker
    result = mapper.map(request)

    # Assert
    assert result is None


def test_mapper_chain_return_command_with_valid_data():
    # Arrange
    expected = RegisterUser(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    request = RegisterUserRequest(
        user_id='018f9284-769b-726d-b3bf-3885bf2ddd3c',
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    mapper = RegisterUserRequestMapper()

    chain = RequestMappersChain()

    # Act
    chain.add(mapper)

    result = chain.map(request)

    # Assert
    assert result == expected


def test_mapper_chain_raise_error_when_no_mapper_added():
    # Arrange
    expected = "No Request Mapper was found for 'RegisterUserRequest'."

    request = RegisterUserRequest(
        user_id='018f9284-769b-726d-b3bf-3885bf2ddd3c',
        name="John Doe Smith",
        slug="john-doe-smith",
    )

    chain = RequestMappersChain()

    # Act
    with pytest.raises(RequestMapperNotFound) as error:
        # noinspection PyTypeChecker
        _ = chain.map(request)

    # Assert
    assert str(error.value) == expected


def test_mapper_chain_raise_error_when_no_mapper_found():
    # Arrange
    expected = "No Request Mapper was found for 'LogInUserRequest'."

    request = LogInUserRequest(
        name="John Doe",
        email="john-doe@example.com",
    )

    mapper = RegisterUserRequestMapper()

    chain = RequestMappersChain()

    # Act
    chain.add(mapper)

    with pytest.raises(RequestMapperNotFound) as error:
        # noinspection PyTypeChecker
        _ = chain.map(request)

    # Assert
    assert str(error.value) == expected
