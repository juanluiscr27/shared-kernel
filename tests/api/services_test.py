from uuid import UUID

from sharedkernel.api.services import AckResponseModel
from sharedkernel.application.commands import Acknowledgement, CommandStatus


def test_ack_response_model_from_acknowledgement():
    # Arrange
    expected = {
        "status": "executed",
        "data": {
            "action": "RegisterUser",
            "entityId": UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
            "version": 1
        }
    }

    ack = Acknowledgement(
        status=CommandStatus.EXECUTED,
        action="RegisterUser",
        entity_id=UUID('018f9284-769b-726d-b3bf-3885bf2ddd3c'),
        version=1,
    )

    # Act
    result = AckResponseModel.from_acknowledgement(ack)

    # Assert
    assert result.model_dump(by_alias=True) == expected
