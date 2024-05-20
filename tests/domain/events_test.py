from dataclasses import dataclass

from sharedkernel.domain.events import DomainEvent


@dataclass(frozen=True)
class AccountOpened(DomainEvent):
    event_id: str
    message: str


def test_entity_qualname():
    # Arrange
    expected = "AccountOpened"

    # Act
    account = AccountOpened('7010054', 'account-opened')

    # Assert
    assert account.qualname == expected


def test_entity_full_qualname():
    # Arrange
    expected = "tests.domain.events_test.AccountOpened"

    # Act
    account = AccountOpened('7010054', 'account-opened')

    # Assert
    assert account.full_qualname == expected
