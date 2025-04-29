from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    product_id: int
    name: str
    price: str
    image: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        orm_mode = True

class ProductDetail(BaseModel):
    product_id: int
    name: str
    price: str
    image: Optional[str] = None
    description: Optional[str] = None
    quantity: int
    rating: float
    
    class Config:
        orm_mode = True
