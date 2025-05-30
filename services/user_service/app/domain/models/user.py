from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


@dataclass
class NewUser:
    username: str
    email: str
    password: str


@dataclass
class UserToCreate:
    username: str
    email: str
    password_hash: str


@dataclass
class UserToUpdate:
    username: str
    email: str


@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    role: UserRole
    created_at: datetime
