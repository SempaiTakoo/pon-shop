from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.domain.models.user import UserRole


class Base(DeclarativeBase):
    pass


class UserORM(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[UserRole]
    created_at: Mapped[datetime]
