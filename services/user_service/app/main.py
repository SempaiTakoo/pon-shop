from typing import Annotated

from fastapi import Depends, FastAPI

from app.api.dependencies import user_service
from app.schemas.user import UserAddSchema
from app.services.user import UserService

app = FastAPI()


@app.post('/users')
def add_user(
    user: UserAddSchema,
    user_service: Annotated[UserService, Depends(user_service)]
):
    user_id = user_service.add_one(user)
    return {'user_id': user_id}
