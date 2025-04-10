from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import Product

class ProductService:
    async def get_products(
        self, 
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None
    ):
        query = select(Product).offset(skip).limit(limit)
        if category_id:
            query = query.where(Product.category_id == category_id)
        
        result = await db.execute(query)
        return result.scalars().all()

    async def get_product(self, db: AsyncSession, product_id: int):
        result = await db.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()