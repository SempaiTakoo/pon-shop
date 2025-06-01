from app.domain.models.order import Order as DomainOrder
from app.db.models import Order as ORMOrder
from app.repository.order import OrderRepository
from app.api.schemas import OrderCreate, OrderUpdate
from app.kafka.producer import send_order_event

def to_domain(orm: ORMOrder):
    return DomainOrder(
        order_id=orm.order_id,
        buyer_id=orm.buyer_id,
        product_id=orm.product_id,
        quantity=orm.quantity,
        status=orm.status,
        created_at=orm.created_at
    )

class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repo = repository

    def get_all_orders(self):
        orms = self.repo.get_all()
        return [to_domain(order) for order in orms]
    
    def get_order(self, order_id: int):
        orm = self.repo.get_by_id(order_id)
        if orm is None:
            return None
        return to_domain(orm)
    
    def add_order(self, order: OrderCreate):
        orm_order = ORMOrder(
            product_id=order.product_id,
            buyer_id=order.buyer_id,
            quantity=order.quantity,
            status=order.status
        )
        created_order = self.repo.add(orm_order)

        event = {
            "event": "order_created",
            "data": {
                "order_id": created_order.order_id,
                "product_id": created_order.product_id,
                "quantity": created_order.quantity
            }
        }
        send_order_event(event)

        return to_domain(created_order)
    
    def update_order(self, order_id: int, data: OrderUpdate):
        updated_order = self.repo.update(order_id, data.model_dump())
        event = {
            "event": "order_updated",
            "data": {
                "order_id": updated_order.order_id,
                "product_id": updated_order.product_id,
                "quantity": updated_order.quantity,
                "status": updated_order.status,
            }
        }
        send_order_event(event)
        return to_domain(updated_order)

    def delete_order(self, order_id: int):
        order = self.repo.get_by_id(order_id)
        if order:
            event = {
                "event": "order_deleted",
                "data": {
                    "order_id": order.order_id
                }
            }
            send_order_event(event)
        self.repo.delete(order_id)
