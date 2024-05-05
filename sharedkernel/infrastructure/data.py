from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class DataModel:
    """DataModel base class

    Is a Data Transfer Object represent cohesive information in the infrastructure optimized for queries.
    """


@dataclass(frozen=True)
class Message:
    message_id: str
    content_type: str
    subject: str
    body: str
