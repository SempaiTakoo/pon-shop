from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from sqlalchemy import ForeignKey, BigInteger, Integer, TIMESTAMP, DECIMAL, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from database import Base

class OrderStatusEnum(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"

class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    #product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.product_id"))
    #buyer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    quantity: Mapped[int] = mapped_column(Integer)
    total_price: Mapped[Decimal] = mapped_column(DECIMAL(12, 2))  
    #status: Mapped[OrderStatusEnum] = mapped_column(SQLEnum(OrderStatusEnum))  
    '''
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now()
    )
    '''