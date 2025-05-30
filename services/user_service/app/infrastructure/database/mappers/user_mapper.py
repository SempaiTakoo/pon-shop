from app.domain.models.user import User
from app.infrastructure.database.models.user import UserORM


def orm_to_user(user: UserORM) -> User:
    return User(
        id=user.id,
        username=user.username,
        email=user.email,
        password_hash=user.password_hash,
        role=user.role,
        created_at=user.created_at,
    )
