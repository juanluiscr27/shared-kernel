import json
from dataclasses import dataclass

from sharedkernel.api.contracts import ErrorResponse, ProblemDetail, DomainErrorResponse
from sharedkernel.domain.errors import Error, UnknownEvent
from sharedkernel.domain.events import DomainEvent
from sharedkernel.domain.models import EntityID, Aggregate


@dataclass(frozen=True)
class UserID(EntityID):
    value: int


class User(Aggregate[UserID]):

    def __init__(self, user_id: UserID, name):
        super().__init__(user_id, 0)
        self.name: str = name


@dataclass(frozen=True)
class AccountOpened(DomainEvent):
    event_id: str
    message: str


def test_problem_detail_is_parsed_to_json():
    # Arrange
    error_dict = {'loc': ["Users.CreateUser"],
                  'msg': "First name is null or empty.",
                  'type': "FirstName.NullOrEmpty", }

    expected = json.dumps(error_dict, separators=(',', ':'))

    # Act
    result = ProblemDetail(loc=["Users.CreateUser"],
                           msg="First name is null or empty.",
                           type="FirstName.NullOrEmpty", )

    # Assert
    assert result.model_dump_json() == expected


def test_problem_detail_is_constructed_with_error_response():
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
    assert result.model_dump_json() == expected.model_dump_json()


def test_problem_detail_is_constructed_with_domain_error():
    # Arrange
    account_opened = AccountOpened('7010054', 'account-opened')

    user_id = UserID(value=101)

    user = User(user_id=user_id, name="John Doe")

    expected = ProblemDetail(loc=["tests.api.contracts_test.User"],
                             msg="Event(AccountOpened) cannot be applied to 'tests.api.contracts_test.User'",
                             type="sharedkernel.domain.errors.UnknownEvent", )

    unknown_event = UnknownEvent(aggregate=user, event=account_opened)

    # Act
    result = DomainErrorResponse(error=unknown_event)

    # Assert
    assert result.json() == expected.json()
