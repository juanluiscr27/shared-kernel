from abc import abstractmethod
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


class Users(Repository[User]):
    @abstractmethod
    def save(self, user: User) -> int:
        ...

    @abstractmethod
    def find_by_id(self, user_id: UserID) -> Optional[UserID]:
        ...

    @abstractmethod
    def find_by_slug(self, slug: str) -> Optional[UserID]:
        ...

    @abstractmethod
    def find_all(self) -> List[User]:
        ...


def test_repository_with_aggregates():
    # Arrange
    expected = "User"

    class TestUsers(Users):

        def save(self, user: User) -> int:
            pass

        def find_by_id(self, user_id: UserID) -> Optional[UserID]:
            pass

        def find_by_slug(self, slug: str) -> Optional[UserID]:
            pass

        def find_all(self) -> List[User]:
            pass

    # Act
    users = TestUsers()

    # Assert
    assert users.aggregate_type == expected
