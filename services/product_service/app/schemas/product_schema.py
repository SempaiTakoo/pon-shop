from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float

class ProductCreate(ProductBase):
    category_id: int

class Product(ProductBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True

class ProductDetail(Product):
    views_count: int
    rating: float | None