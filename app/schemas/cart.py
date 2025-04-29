from typing import List, Optional
from pydantic import BaseModel

class CartItem(BaseModel):
    product_id: int
    name: str
    quantity: int
    price: str
    total_price: str
    
    class Config:
        orm_mode = True

class CartAdd(BaseModel):
    product_id: int
    quantity: int = 1

class CartRemove(BaseModel):
    product_id: int

class CartItemList(BaseModel):
    items: List[CartItem]
    total_price: str
    
    class Config:
        orm_mode = True

class CartResponse(BaseModel):
    status: str
    data: CartItemList