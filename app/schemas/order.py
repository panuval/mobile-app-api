from typing import List, Optional
from pydantic import BaseModel

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Address(BaseModel):
    address_1: str
    address_2: Optional[str] = None
    city: str
    postcode: str
    country: str

class PaymentDetails(BaseModel):
    card_number: str
    expiry_date: str
    cvv: str

class OrderCreate(BaseModel):
    user_id: int
    cart_items: List[OrderItem]
    billing_address: Address
    payment_method: str
    payment_details: PaymentDetails

class OrderItemResponse(BaseModel):
    product_id: int
    name: str
    quantity: int
    price: str

class OrderDetail(BaseModel):
    order_id: int
    status: str
    items: List[OrderItemResponse]
    total_price: str

class OrderResponse(BaseModel):
    status: str
    order_id: int
    total_price: str
