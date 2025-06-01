from app.domain.interfaces.user_repository import UserRepository
from app.domain.models.user import NewUser, User, UserToCreate, UserToUpdate
from app.infrastructure.kafka_logger import KafkaLogger
from app.config import settings


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository
        self.logger = KafkaLogger(
            broker_url=settings.KAFKA_BROKER_URL,
            topic=settings.KAFKA_LOG_TOPIC
        )

    def create_one(self, new_user: NewUser) -> User:
        user_to_create = UserToCreate(
            username=new_user.username,
            email=new_user.email,
            password_hash=new_user.password,
        )
        created_user = self.user_repo.create_one(user_to_create)
        self.logger.log(
            event='CREATE',
            data={'user': created_user.__dict__}
        )
        return created_user

    def get_by_id(self, user_id: int) -> User | None:
        user = self.user_repo.get_by_id(user_id)
        if user:
            self.logger.log(
                event='READ',
                data={'user_id': user_id}
            )
        return user

    def get_all(self) -> list[User]:
        users = self.user_repo.get_all()
        self.logger.log(
            event='READ ALL',
            data={'count': len(users)}
        )
        return users

    def update(self, user_id: int, user_to_update: UserToUpdate) -> User | None:
        updated_user = self.user_repo.update(user_id, user_to_update)
        if updated_user:
            self.logger.log(
                event='UPDATE',
                data={'user_id': user_id}
            )
        return updated_user

    def delete(self, user_id: int) -> bool:
        is_user_deleted = self.user_repo.delete(user_id)
        if is_user_deleted:
            self.logger.log(
                event='DELETE',
                data={'user_id': user_id}
            )
        return is_user_deleted
