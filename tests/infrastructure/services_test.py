import json
from datetime import datetime, timezone, timedelta
from uuid import UUID

from sharedkernel.infrastructure.services import UUIDEncoder, DateTimeEncoder, ExtraEncoder


def test_serialize_uuid_return_encoded_value():
    # Arrange
    expected = '{"value": "0191b0c5-8300-7c60-9700-f14bf5475624"}'

    value = {'value': UUID('0191b0c5-8300-7c60-9700-f14bf5475624')}

    # Act
    result = json.dumps(value, cls=UUIDEncoder)

    # Assert
    assert result == expected


def test_serialize_datetime_return_encoded_value():
    # Arrange
    expected = '{"value": "2006-05-31T01:30:45-04:00"}'

    value = {
        'value': datetime(
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
    result = json.dumps(value, cls=DateTimeEncoder)

    # Assert
    assert result == expected


def test_serialize_extra_types_return_encoded_value():
    # Arrange
    expected = '{"value1": "0191b0c5-8300-7c60-9700-f14bf5475624", "value2": "2006-05-31T01:30:45-04:00"}'

    value = {
        'value1': UUID('0191b0c5-8300-7c60-9700-f14bf5475624'),
        'value2': datetime(
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
    result = json.dumps(value, cls=ExtraEncoder)

    # Assert
    assert result == expected
