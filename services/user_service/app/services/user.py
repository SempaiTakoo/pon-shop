

from app.repositories.base import AbstractRepository
from app.schemas.user import UserAddSchema


class UserService:
    def __init__(self, user_repository: type[AbstractRepository]):
        self.user_repo = user_repository()

    def add_one(self, user: UserAddSchema) -> int:
        user_dict = user.model_dump()
        user_id = self.user_repo.add_one(user_dict)
        return user_id

    def get_all(self):
        return self.user_repo.get_all()
