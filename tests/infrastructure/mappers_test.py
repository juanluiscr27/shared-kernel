from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID

from sharedkernel.domain.events import DomainEvent
from sharedkernel.infrastructure.data import Event
from sharedkernel.infrastructure.mappers import Mapper, MappersChain, MappingPipeline, extract, to_event


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


def test_extract_json_string_from_quoted_json_string():
    # Arrange
    expected = '{\"user_id\": \"018f9284-769b-726d-b3bf-3885bf2ddd3c\", \"email\": \"john-doe@example.com\"}'

    quoted_json_str = ('"{\\"user_id\\": \\"018f9284-769b-726d-b3bf-3885bf2ddd3c\\", \\"email\\": '
                       '\\"john-doe@example.com\\"}"')

    # Act
    result = extract(quoted_json_str)

    # Assert
    assert result == expected


def test_extract_return_same_json_string():
    # Arrange
    expected = '{\"user_id\": \"018f9284-769b-726d-b3bf-3885bf2ddd3c\", \"email\": \"john-doe@example.com\"}'

    # Act
    result = extract(expected)

    # Assert
    assert result == expected


def test_deserialize_json_string_to_event():
    # Arrange
    expected = Event(
        event_id=UUID("018ff859-d78c-4dc8-e0d2-4094d208a18c"),
        event_type="OfficialNameUpdated",
        position=4,
        data="{\"official_id\": \"018fdb92-75b9-2616-9a6c-720aae66a022\", \"new_name\": \"John Doe IV\", "
             "\"previous_name\": \"John Doe III\"}",
        stream_id=UUID("018fdb92-75b9-2616-9a6c-720aae66a022"),
        stream_type="Official",
        version=7,
        created=datetime.fromisoformat("2024-06-08 14:56:28.542193+00"),
        correlation_id=UUID("018ff859-d78b-c284-3284-b7cbd0a31642"),
    )

    obj_dict = {
        "id": "018ff859-d78c-4dc8-e0d2-4094d208a18c",
        "type": "OfficialNameUpdated",
        "position": 4,
        "data": '"{\\"official_id\\": \\"018fdb92-75b9-2616-9a6c-720aae66a022\\", \\"new_name\\": \\"John Doe IV\\", '
                '\\"previous_name\\": \\"John Doe III\\"}"',
        "stream_id": "018fdb92-75b9-2616-9a6c-720aae66a022",
        "stream_type": "Official",
        "version": 7,
        "created": "2024-06-08 14:56:28.542193+00",
        "correlation_id": "018ff859-d78b-c284-3284-b7cbd0a31642"
    }

    # Act
    result = to_event(obj_dict, None)

    # Assert
    assert result == expected


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


def test_mapper_chain_return_none_when_different_mapper_added():
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


def test_mapper_chain_return_none_when_no_mapper_added():
    # Arrange
    registered_data = {"user_id": "018f9284-769b-726d-b3bf-3885bf2ddd3c", "email": "john-doe@example.com"}
    registered_type = "UserRegistered"

    chain = MappersChain()

    # Act
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


def test_mapping_pipeline_return_event_when_no_mapping_behavior():
    # Arrange
    registered_data = {"user_id": "018f9284-769b-726d-b3bf-3885bf2ddd3c", "email": "john-doe@example.com"}
    registered_type = "UserRegistered"

    # Act
    pipeline = MappingPipeline()

    result = pipeline.map(registered_data, registered_type)

    # Assert
    assert result is None
