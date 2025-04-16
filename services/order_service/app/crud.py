from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import Order
from app.schemas import OrderCreate, OrderUpdate

def create_order(order_data: OrderCreate, db: Session):
    order_values = order_data.model_dump()
    db_order = Order(**order_values)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session):
    return db.query(Order).all()

def get_order(order_id: int, db: Session):
    return db.query(Order).filter(Order.order_id == order_id).first()

def delete_order(order: Order, db: Session):
    db.delete(order)
    db.commit()
    return order

def update_order(order: Order, order_data: OrderUpdate, db: Session):
    update_data = order_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order