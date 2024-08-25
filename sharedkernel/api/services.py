from dataclasses import dataclass

from sharedkernel.api.contracts import AckResponse, AckData
from sharedkernel.application.commands import Acknowledgement


@dataclass
class ElapsedTime:
    value: float

    @classmethod
    def from_delta(cls, start: float, end: float):
        return cls(end - start)

    @property
    def milliseconds(self):
        return round(self.value * 1000)


class AckResponseModel:
    @staticmethod
    def from_acknowledgement(ack: Acknowledgement) -> AckResponse:
        data = AckData(
            action=ack.action,
            entityId=ack.entity_id,
            version=ack.version,
        )

        return AckResponse(status=ack.status, data=data)
