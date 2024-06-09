from sharedkernel.application.errors import ErrorDetail


def test_error_detail_is_parsed_dictionary():
    # Arrange
    expected = {'loc': ['Users.CreateUser'],
                'msg': 'First name is null or empty.',
                'type': 'FirstName.NullOrEmpty', }

    # Act
    result = ErrorDetail(loc=["Users.CreateUser"],
                         msg="First name is null or empty.",
                         type="FirstName.NullOrEmpty", )

    # Assert
    assert result.asdict() == expected
