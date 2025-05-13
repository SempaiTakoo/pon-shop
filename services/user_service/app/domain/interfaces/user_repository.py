from abc import ABC, abstractmethod

from app.domain.models.user import User, UserToCreate, UserToUpdate


class UserRepository(ABC):
    @abstractmethod
    def create_one(self, user_to_create: UserToCreate) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def get_all(self) -> list[User]:
        pass

    @abstractmethod
    def update(self, user_id: int, user_to_update: UserToUpdate) -> User | None:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass
