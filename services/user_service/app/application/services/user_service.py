import threading
import time

from app.config import settings
from app.domain.interfaces.user_repository import UserRepository
from app.domain.models.user import NewUser, User, UserToCreate, UserToUpdate
from app.infrastructure.database.models.user import UserReviewCountORM
from app.infrastructure.database.session import session_maker
from app.infrastructure.kafka_logger import MessageBrokerConsumer, MessageBrokerLogger


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository
        self.logger = MessageBrokerLogger(
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
            data={
                'user': {
                    'created_user.id': created_user.id,
                    'created_user.username': created_user.username,
                    'created_user.role': created_user.role,
                    'created_user.email': created_user.email
                }
            }
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


class ReviewCountUpdater:
    def __init__(self, broker_url: str, topic: str):
        self.consumer = MessageBrokerConsumer(broker_url, topic)
        self._stop_event = threading.Event()

    def handle_event(self, event_data):
        event_type = event_data.get('event_type')
        user_id = event_data.get('user_id')

        if not user_id:
            return

        with session_maker() as session:
            obj = session.get(UserReviewCountORM, user_id)
            if event_type == 'review_created':
                if obj:
                    obj.review_count += 1
                else:
                    obj = UserReviewCountORM(user_id=user_id, review_count=1)
                    session.add(obj)
            elif event_type == 'review_deleted':
                if obj and obj.review_count > 0:
                    obj.review_count -= 1
            session.commit()

    def run(self):
        while not self._stop_event.is_set():
            self.consumer.consume_logs(self.handle_event)
            time.sleep(1)

    def stop(self):
        self._stop_event.set()
