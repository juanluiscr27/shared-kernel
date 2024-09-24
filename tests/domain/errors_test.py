from sharedkernel.domain.errors import Error


def test_error_is_parsed_to_dictionary():
    # Arrange
    expected = {"message": "First name is null or empty.",
                "code": "FirstName.NullOrEmpty",
                "reason": f"User 'first name' should not be null nor empty.",
                "domain": "Users.CreateUser", }

    error = Error(
        message="First name is null or empty.",
        code="FirstName.NullOrEmpty",
        reason=f"User 'first name' should not be null nor empty.",
        domain="Users.CreateUser", )

    # Act
    result = error.to_dict()

    # Assert
    assert result == expected
