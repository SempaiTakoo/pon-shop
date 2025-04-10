from app.models.user import User
from app.repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
