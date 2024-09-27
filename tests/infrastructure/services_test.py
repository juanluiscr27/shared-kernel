import json
from datetime import datetime, timezone, timedelta
from uuid import UUID

from sharedkernel.infrastructure.services import UUIDEncoder, DateTimeEncoder, ExtraEncoder


def test_serialize_uuid_return_encoded_value():
    # Arrange
    expected = '{"id": "0191b0c5-8300-7c60-9700-f14bf5475624", "price": 100}'

    data = {'id': UUID('0191b0c5-8300-7c60-9700-f14bf5475624'), 'price': 100}

    # Act
    result = json.dumps(data, cls=UUIDEncoder)

    # Assert
    assert result == expected


def test_serialize_datetime_return_encoded_value():
    # Arrange
    expected = '{"price": 100, "date": "2006-05-31T01:30:45-04:00"}'

    data = {
        'price': 100,
        'date': datetime(
            year=2006,
            month=5,
            day=31,
            hour=1,
            minute=30,
            second=45,
            tzinfo=timezone(timedelta(hours=-4)),
        ),
    }

    # Act
    result = json.dumps(data, cls=DateTimeEncoder)

    # Assert
    assert result == expected


def test_serialize_extra_types_return_encoded_value():
    # Arrange
    expected = '{"id": "0191b0c5-8300-7c60-9700-f14bf5475624", "price": 100, "date": "2006-05-31T01:30:45-04:00"}'

    data = {
        'id': UUID('0191b0c5-8300-7c60-9700-f14bf5475624'),
        'price': 100,
        'date': datetime(
            year=2006,
            month=5,
            day=31,
            hour=1,
            minute=30,
            second=45,
            tzinfo=timezone(timedelta(hours=-4)),
        )
    }

    # Act
    result = json.dumps(data, cls=ExtraEncoder)

    # Assert
    assert result == expected
