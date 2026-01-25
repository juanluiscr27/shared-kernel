from dataclasses import dataclass

from sharedkernel.api.contracts import AckResponse, AckData
from sharedkernel.application.commands import Acknowledgement


@dataclass
class ElapsedTime:
    """Represents the elapsed time of an operation.

    Attributes:
        value: The elapsed time in seconds.
    """
    value: float

    @classmethod
    def from_delta(cls, start: float, end: float) -> "ElapsedTime":
        """Creates an ElapsedTime instance from a start and end time.

        Args:
            start: The start time in seconds.
            end: The end time in seconds.
        """
        return cls(end - start)

    @property
    def milliseconds(self) -> int:
        """Returns the elapsed time in milliseconds."""
        return round(self.value * 1000)


class AckResponseModel:
    """Utility class to create AckResponse objects."""

    @staticmethod
    def from_acknowledgement(ack: Acknowledgement) -> AckResponse:
        """Creates an AckResponse from a command acknowledgement.

        Args:
            ack: The command acknowledgement.

        Returns:
            An AckResponse object.
        """
        data = AckData(
            action=ack.action,
            entityId=ack.entity_id,
            version=ack.version,
        )

        return AckResponse(status=ack.status, data=data)
