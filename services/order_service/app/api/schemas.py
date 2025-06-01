from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class OrderStatusEnum(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"

class OrderBase(BaseModel):
    product_id: int = Field(..., gt=0)
    buyer_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    status: OrderStatusEnum

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0, description="New quantity, must be > 0")
    status: Optional[OrderStatusEnum] = Field(None, description="New order status")