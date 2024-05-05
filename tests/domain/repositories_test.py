from dataclasses import dataclass
from typing import List, Optional

from sharedkernel.domain.models import Aggregate, EntityID
from sharedkernel.domain.repositories import Repository


@dataclass(frozen=True)
class UserID(EntityID):
    value: int


class User(Aggregate[UserID]):

    def __init__(self, user_id: UserID, name):
        super().__init__(user_id, 0)
        self.name: str = name


def test_repository_with_aggregates():
    # Arrange
    expected = "tests.domain.repositories_test.User"

    class Users(Repository[User]):

        def save(self, user: User):
            pass

        def find_by_id(self, user_id: UserID) -> Optional[UserID]:
            pass

        def find_by_slug(self, slug: str) -> Optional[UserID]:
            pass

        def find_all(self) -> List[User]:
            pass

    # Act
    users = Users()

    # Assert
    assert users.aggregate_type == expected
