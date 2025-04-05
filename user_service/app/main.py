from fastapi import FastAPI
from database import get_db_version

app = FastAPI()


@app.get('/')
def index():
    db_version = get_db_version()
    return f'User service db version: {db_version}'
