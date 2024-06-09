from dataclasses import dataclass


@dataclass
class ElapsedTime:
    value: float

    @classmethod
    def from_delta(cls, start: float, end: float):
        return cls(end - start)

    @property
    def milliseconds(self):
        return round(self.value * 1000)
