from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import Order, OrderProduct

class OrderService:
    async def get_order(self, db: AsyncSession, order_id: int):
        result = await db.execute(
            select(Order).where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_order_products(self, db: AsyncSession, order_id: int):
        result = await db.execute(
            select(OrderProduct)
            .where(OrderProduct.order_id == order_id)
            .join(OrderProduct.product)
        )
        return result.scalars().all()