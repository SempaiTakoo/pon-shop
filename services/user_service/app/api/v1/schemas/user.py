from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.domain.models.user import UserRole


class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    users: list[UserResponse]

    model_config = ConfigDict(from_attributes=True)


class UserUpdateRequest(BaseModel):
    username: str
    email: EmailStr
