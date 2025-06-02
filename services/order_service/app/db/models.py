from typing import Optional
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from sqlalchemy import ForeignKey, BigInteger, Integer, DateTime, DECIMAL, Text, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.session import Base

class OrderStatusEnum(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"

class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    buyer_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer)
    total_price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(12, 2), nullable=True)
    status: Mapped[OrderStatusEnum] = mapped_column(SQLEnum(OrderStatusEnum))  
    created_at:  Mapped[datetime]  = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )