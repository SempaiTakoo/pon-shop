from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services.user_service import UserService
from app.infrastructure.database.repositories.user_repository_impl import (
    SQLAlchemyUserRepository,
)
from app.infrastructure.database.session import get_db
from app.application.services.user_service import ReviewCountUpdater



def get_user_service(session: Annotated[Session, Depends(get_db)]) -> UserService:
    user_repo = SQLAlchemyUserRepository(session)
    user_service = UserService(user_repo)
    return user_service


def start_review_count_updater(broker_url: str, topic: str):
    review_count_updater = ReviewCountUpdater(broker_url=broker_url, topic=topic)
    review_count_updater.run()
