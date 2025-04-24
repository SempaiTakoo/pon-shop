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
