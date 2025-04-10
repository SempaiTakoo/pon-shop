from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..services import order_service
from ..schemas import order_schema
from ..dependencies import get_db

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/{order_id}/products/", response_model=List[order_schema.OrderProduct])
async def get_order_products(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить список продуктов в заказе"""
    order = await order_service.get_order(db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return await order_service.get_order_products(db, order_id=order_id)