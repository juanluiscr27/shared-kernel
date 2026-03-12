from dataclasses import dataclass

from sharedkernel.application.queries import Query


@dataclass(frozen=True)
class GetUserByID(Query):
    user_id: str


def test_query_qualname():
    # Arrange
    expected = "GetUserByID"

    # Act
    query = GetUserByID(user_id="018f9284")

    # Assert
    assert query.qualname == expected


def test_query_full_qualname():
    # Arrange
    expected = "tests.application.queries_test.GetUserByID"

    # Act
    query = GetUserByID(user_id="018f9284")

    # Assert
    assert query.full_qualname == expected
