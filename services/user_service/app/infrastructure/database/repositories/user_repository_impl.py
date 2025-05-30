import datetime
from sqlalchemy.orm import Session

from app.domain.interfaces.user_repository import UserRepository
from app.domain.models.user import User, UserRole, UserToCreate, UserToUpdate
from app.infrastructure.database.mappers.user_mapper import orm_to_user
from app.infrastructure.database.models.user import UserORM


class SQLAlchemyUserRepository(UserRepository):
    model_orm = UserORM

    def __init__(self, session: Session):
        self.session = session

    def create_one(self, user_to_create: UserToCreate) -> User:
        with self.session.begin():
            user_orm = UserORM(
                username=user_to_create.username,
                email=user_to_create.email,
                password_hash=user_to_create.password_hash,
                role=UserRole.user,
                created_at=datetime.datetime.now()
            )
            self.session.add(user_orm)
            self.session.flush()
            self.session.refresh(user_orm)
            return orm_to_user(user_orm)

    def get_by_id(self, user_id: int) -> User | None:
        user_orm = self.session.get(self.model_orm, user_id)
        if not user_orm:
            return None
        return orm_to_user(user_orm)

    def get_all(self) -> list[User]:
        users_orm = self.session.query(self.model_orm).all()
        users = [orm_to_user(user_orm) for user_orm in users_orm]
        return users

    def update(self, user_id: int, user_to_update: UserToUpdate) -> User | None:
        with self.session.begin():
            user_orm = self.session.get(self.model_orm, user_id)
            if not user_orm:
                return None
            user_orm.username = user_to_update.username
            user_orm.email = user_to_update.email
            self.session.add(user_orm)
            self.session.flush()
            self.session.refresh(user_orm)
            return orm_to_user(user_orm)

    def delete(self, user_id: int) -> bool:
        with self.session.begin():
            user_orm = self.session.get(self.model_orm, user_id)
            if not user_orm:
                return False
            self.session.delete(user_orm)
            self.session.flush()
            return True
