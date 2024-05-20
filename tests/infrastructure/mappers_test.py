from dataclasses import dataclass
from typing import Dict, Any, Optional
from uuid import UUID

from sharedkernel.domain.events import DomainEvent
from sharedkernel.infrastructure.mappers import Mapper, MappersChain, MappingPipeline


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    user_id: UUID
    email: str


@dataclass(frozen=True)
class UserLoggedIn(DomainEvent):
    name: str
    email: str


class UserRegisteredMapper(Mapper[UserRegistered]):

    def map(self, data: Dict[str, Any], event_type: str) -> Optional[UserRegistered]:
        if event_type != self.event_type:
            return self.map_next(data, event_type)

        return UserRegistered(
            user_id=UUID(data['user_id']),
            email=data['email'],
        )


class UserLoggedInMapper(Mapper[UserLoggedIn]):

    def map(self, data: Dict[str, Any], event_type: str) -> Optional[UserLoggedIn]:
        if event_type == self.event_type:
            return UserLoggedIn(
                name=data['name'],
                email=data['email'],
            )

        return self.map_next(data, event_type)


def test_mapper_return_domain_event_with_valid_data():
    # Arrange
    expected = UserRegistered(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        email="john-doe@example.com",
    )

    data = {"user_id": "018f9284-769b-726d-b3bf-3885bf2ddd3c", "email": "john-doe@example.com"}
    event_type = "UserRegistered"

    mapper = UserRegisteredMapper()

    # Act

    result = mapper.map(data, event_type)

    # Assert
    assert result == expected


def test_mapper_return_none_with_invalid_data():
    # Arrange
    data = {"name": "John Doe", "email": "john-doe@example.com"}
    event_type = "UserLoggedIn"

    mapper = UserRegisteredMapper()

    # Act

    result = mapper.map(data, event_type)

    # Assert
    assert result is None


def test_mapper_chain_return_events_with_valid_data():
    # Arrange
    user_registered = UserRegistered(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        email="john-doe@example.com",
    )

    user_logged_in = UserLoggedIn(
        name="John Doe",
        email="john-doe@example.com",
    )

    registered_data = {"user_id": "018f9284-769b-726d-b3bf-3885bf2ddd3c", "email": "john-doe@example.com"}
    registered_type = "UserRegistered"

    logged_in_data = {"name": "John Doe", "email": "john-doe@example.com"}
    logged_in_type = "UserLoggedIn"

    registered_mapper = UserRegisteredMapper()
    logged_in_mapper = UserLoggedInMapper()

    chain = MappersChain()

    # Act
    chain.add(registered_mapper)
    chain.add(logged_in_mapper)

    registered_result = chain.map(registered_data, registered_type)
    logged_in_result = chain.map(logged_in_data, logged_in_type)

    # Assert
    assert registered_result == user_registered
    assert logged_in_result == user_logged_in


def test_mapper_chain_return_none_when_no_mapper_added():
    # Arrange
    registered_data = {"user_id": "018f9284-769b-726d-b3bf-3885bf2ddd3c", "email": "john-doe@example.com"}
    registered_type = "UserRegistered"

    logged_in_mapper = UserLoggedInMapper()

    chain = MappersChain()

    # Act
    chain.add(logged_in_mapper)

    result = chain.map(registered_data, registered_type)

    # Assert
    assert result is None


def test_mapping_pipeline_return_event_with_valid_data():
    # Arrange
    expected = UserRegistered(
        user_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        email="john-doe@example.com",
    )

    registered_data = {"user_id": "018f9284-769b-726d-b3bf-3885bf2ddd3c", "email": "john-doe@example.com"}
    registered_type = "UserRegistered"

    registered_mapper = UserRegisteredMapper()
    logged_in_mapper = UserLoggedInMapper()

    chain = MappersChain()
    chain.add(registered_mapper)
    chain.add(logged_in_mapper)

    # Act
    pipeline = MappingPipeline()
    pipeline.register(chain)

    result = pipeline.map(registered_data, registered_type)

    # Assert
    assert result == expected
