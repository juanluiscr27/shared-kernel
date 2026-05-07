from dataclasses import dataclass

from sharedkernel.domain.errors import Error
from sharedkernel.domain.exceptions import ConcurrencyConflict, InvalidState


def test_error_is_parsed_to_dictionary():
    # Arrange
    expected = {"message": "First name is null or empty.",
                "code": "FirstName.NullOrEmpty",
                "reason": "User 'first name' should not be null nor empty.",
                "domain": "Users.CreateUser", }

    error = Error(
        message="First name is null or empty.",
        code="FirstName.NullOrEmpty",
        reason="User 'first name' should not be null nor empty.",
        domain="Users.CreateUser", )

    # Act
    result = error.to_dict()

    # Assert
    assert result == expected


def test_invalid_state_exception_sets_attributes():
    # Arrange
    @dataclass
    class Order:
        order_id: str

    source = Order(order_id="ORD-001")

    # Act
    error = InvalidState(
        source=source,
        message="Order cannot be cancelled.",
        code="Order.State.Invalid",
        reason="Order 'ORD-001' has already been shipped.",
    )

    # Assert
    assert str(error) == "Order cannot be cancelled."
    assert error.code == "Order.State.Invalid"
    assert error.reason == "Order 'ORD-001' has already been shipped."
    assert "Order" in error.domain


def test_concurrency_conflict_exception_sets_attributes():
    # Arrange
    @dataclass
    class Account:
        account_id: str

    source = Account(account_id="ACC-001")

    # Act
    error = ConcurrencyConflict(source=source, entity_id="ACC-001", version=3)

    # Assert
    assert "ACC-001" in str(error)
    assert error.code == "Account.Conflict"
    assert "version 3" in error.reason
    assert "Account" in error.domain
