from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Role(Enum):
    user = 'user'
    admin = 'admin'


@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    role: Role
    created_at: datetime
