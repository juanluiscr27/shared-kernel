from dataclasses import dataclass

from sharedkernel.api.contracts import ErrorResponse, ProblemDetail
from sharedkernel.domain.errors import Error, UnknownEvent


def test_problem_detail_is_constructed_with_error():
    # Arrange
    expected = ProblemDetail(loc=["Users.CreateUser"],
                             msg="First name is null or empty.",
                             type="FirstName.NullOrEmpty", )

    null_or_empty = Error(
        message="First name is null or empty.",
        code="FirstName.NullOrEmpty",
        reason=f"User 'first name' should not be null nor empty.",
        domain="Users.CreateUser", )

    # Act
    result = ErrorResponse(error=null_or_empty)

    # Assert
    assert result.json() == expected.json()

