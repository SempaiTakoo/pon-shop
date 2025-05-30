from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services.user_service import UserService
from app.infrastructure.database.repositories.user_repository_impl import (
    SQLAlchemyUserRepository,
)
from app.infrastructure.database.session import get_db


def get_user_service(session: Annotated[Session, Depends(get_db)]) -> UserService:
    user_repo = SQLAlchemyUserRepository(session)
    user_service = UserService(user_repo)
    return user_service
