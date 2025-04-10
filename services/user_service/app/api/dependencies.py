from app.repositories.user import UserRepository
from app.services.user import UserService


def user_service() -> UserService:
    return UserService(UserRepository)
