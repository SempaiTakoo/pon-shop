from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import OrderCreate
from database import SessionLocal, engine
import uvicorn
import crud as crud
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def hello_index():
    return {
        "message": "Hello",
    }


@app.post("/orders/", tags=["Заказы"], summary="Создать заказ")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        db_order = crud.create_order(order, db)
        return db_order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/orders", tags=["Заказы"], summary="Получить все заказы")
def get_orders(db: Session = Depends(get_db)):
    orders = crud.get_orders(db)
    return orders

@app.get("/orders/{id}", tags=["Заказы"], summary="Получить заказ")
def get_order(id, db: Session = Depends(get_db)):
    order = crud.get_order(id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Заказа нет")
    return order

@app.delete("/orders/{id}", tags=["Заказы"], summary="Удалить заказ")
def delete_order(id, db: Session = Depends(get_db)):
    order = crud.get_order(id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Заказа нет")
    order = crud.delete_order(order, db)
    return order

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

