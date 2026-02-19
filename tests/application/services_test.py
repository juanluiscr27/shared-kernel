import pytest

from sharedkernel.application.services import get_status_code


@pytest.mark.parametrize("error_code, expected", [
    ("Coach.Id.NotFound", 404),
    ("Coach.Slug.NotUnique", 409),
    ("Season.Status.Conflict", 409),
    ("Roster.PlayerId.AlreadyOnTeam", 409),
    ("Draft.Round.InvalidValue", 422),
    ("Season.Stage.IsClosed", 409),
])
def test_get_status_code_maps_error_code_to_http_status(error_code, expected):
    # Act
    result = get_status_code(error_code)

    # Assert
    assert result == expected
