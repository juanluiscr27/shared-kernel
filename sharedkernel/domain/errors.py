from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Error:
    """Error Model

    Represents an application error. Commonly used when a validation fails or
    an application rule is broken.

    Args:
        code: Identifies the problem type.
        message: A short summary to describe the type of problem in general.
        reason: A human-readable explanation specific to this occurrence of the problem.
        domain: A reference that identifies the specific instance where the problem occurred.
    """

    code: str
    message: str
    reason: str
    domain: str

    def to_dict(self) -> dict[str, Any]:
        """Converts the error model to a dictionary.

        Returns:
            A dictionary representation of the error.
        """
        return asdict(self)
