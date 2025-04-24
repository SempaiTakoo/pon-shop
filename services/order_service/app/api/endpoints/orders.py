from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.api.schemas import OrderCreate, OrderUpdate
from app.db.session import get_db
from app.service.order_service import OrderService
from app.repository.order import OrderRepository

router = APIRouter(prefix="/orders", tags=["Заказы"])

def get_order_service(db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    return OrderService(repo)

@router.post("/", summary="Создать заказ")
def create_order(order_data: OrderCreate, service: OrderService = Depends(get_order_service)):
    return service.add_order(order_data)


@router.get("/", summary="Получить все заказы")
def get_orders(service: OrderService = Depends(get_order_service)):
    return service.get_all_orders()

@router.get("/{id}", summary="Получить заказ")
def get_order(id, service: OrderService = Depends(get_order_service)):
    order = service.get_order(id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказа нет")
    return order

@router.delete("/{id}", summary="Удалить заказ")
def delete_order(id, service: OrderService = Depends(get_order_service)):
    order = service.get_order(id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказа нет")
    order = service.delete_order(id)
    return order

@router.patch("/{id}", summary="Обновить заказ")
def update_order(id, order_data: OrderUpdate, service: OrderService = Depends(get_order_service)):
    order = service.get_order(id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказа нет")
    order = service.update_order(id, order_data)
    return order