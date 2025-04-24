from app.domain.models.order import Order as DomainOrder
from app.db.models import Order as ORMOrder
from app.repository.order import OrderRepository
from app.api.schemas import OrderCreate, OrderUpdate

def to_domain(orm: ORMOrder):
    return DomainOrder(
        order_id=orm.order_id,
        buyer_id=orm.buyer_id,
        product_id=orm.product_id,
        quantity=orm.quantity,
        total_price=orm.total_price,
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
        total_price=order.total_price,
        status=order.status
        )
        return to_domain(self.repo.add(orm_order))
    
    def update_order(self, order_id: int, data: OrderUpdate):
        return to_domain(self.repo.update(order_id, data.model_dump()))
    
    def delete_order(self, order_id: int):
        self.repo.delete(order_id)

