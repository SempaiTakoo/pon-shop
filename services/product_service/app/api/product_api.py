from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ..services import product_service, order_service
from ..schemas import product_schema, order_schema
from ..dependencies import get_db

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[product_schema.Product])
async def list_products(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Получить список продуктов с пагинацией и фильтрацией по категории"""
    return await product_service.get_products(db, skip=skip, limit=limit, category_id=category_id)

@router.get("/{product_id}/", response_model=product_schema.ProductDetail)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить детальную информацию о продукте"""
    product = await product_service.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product