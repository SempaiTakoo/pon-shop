from app.domain.interfaces.user_repository import UserRepository
from app.domain.models.user import NewUser, User, UserToCreate, UserToUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    def create_one(self, new_user: NewUser) -> User:
        user_to_create = UserToCreate(
            username=new_user.username,
            email=new_user.email,
            password_hash=new_user.password,
        )
        return self.user_repo.create_one(user_to_create)

    def get_by_id(self, user_id: int) -> User | None:
        return self.user_repo.get_by_id(user_id)

    def get_all(self) -> list[User]:
        return self.user_repo.get_all()

    def update(self, user_id: int, user_to_update: UserToUpdate) -> User | None:
        return self.user_repo.update(user_id, user_to_update)

    def delete(self, user_id: int) -> bool:
        return self.delete(user_id)
