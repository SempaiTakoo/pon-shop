from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    
    category = relationship("Category", back_populates="products")
    seller = relationship("Seller", back_populates="products")
    reviews = relationship("Review", back_populates="product")