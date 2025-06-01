from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.endpoints.dependencies import get_user_service
from app.api.v1.schemas.user import (
    UserCreateRequest,
    UserListResponse,
    UserResponse,
    UserUpdateRequest,
)
from app.application.services.user_service import UserService
from app.domain.models.user import NewUser, User, UserToUpdate
from app.infrastructure.database.session import get_db
from app.infrastructure.database.models.user import UserReviewCountORM

router = APIRouter()


@router.post('/')
def add_user(
    user_in: UserCreateRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    new_user = NewUser(
        username=user_in.username, email=user_in.email, password=user_in.password
    )
    user: User = user_service.create_one(new_user)
    print(f'{user=}')
    return UserResponse.model_validate(user)


@router.get('/')
def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserListResponse:
    users: list[User] = user_service.get_all()
    user_responses = [UserResponse.model_validate(user) for user in users]
    return UserListResponse(users=user_responses)


@router.get('/{user_id}')
def get_user(
    user_id: int, user_service: Annotated[UserService, Depends(get_user_service)]
) -> UserResponse | None:
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден.')
    return UserResponse.model_validate(user)


@router.patch('/{user_id}')
def update_user(
    user_id: int,
    user_in: UserUpdateRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse | None:
    user_to_update = UserToUpdate(username=user_in.username, email=user_in.email)
    user = user_service.update(user_id, user_to_update)
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден.')
    return UserResponse.model_validate(user)


@router.delete('/{user_id}')
def delete_user(
    user_id: int, user_service: Annotated[UserService, Depends(get_user_service)]
) -> dict[str, str] | None:
    is_deleted = user_service.delete(user_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail='Пользователь не найден.')
    return {'message': f'Пользователь с id {user_id} был удалён'}


@router.get('/{user_id}/review_count')
def get_review_count(
    user_id: int, db: Annotated[Session, Depends(get_db)]
):
    obj = db.get(UserReviewCountORM, user_id)
    return {"user_id": user_id, "review_count": obj.review_count if obj else 0}
