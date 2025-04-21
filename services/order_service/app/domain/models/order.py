from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class OrderStatus(Enum):
    PENDING = 'pending'
    PAID = 'paid'
    SHIPPED = 'shipped'


@dataclass
class Order:
    order_id: Optional[int]
    product_id: int
    buyer_id: int
    quantity: int
    total_price: float
    status: OrderStatus
    created_at: datetime

    def update_status(self, new_status: OrderStatus):
        self.status = new_status

    def update_quantity(self, new_quantity: int):
        self.quantity = new_quantity

    def update_price(self, new_price: int):
        self.price = new_price
