from pydantic import BaseModel, EmailStr

from app.models.user import Role


class UserAddSchema(BaseModel):
    username: str
    email: EmailStr
    role: Role
