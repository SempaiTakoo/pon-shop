from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import engine
from app.api.endpoints import orders
import app.db.models as models
import uvicorn


app = FastAPI()

app.include_router(orders.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

