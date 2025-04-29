from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.db.database import Base

class Order(Base):
    __tablename__ = "oc_order"
    
    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    firstname = Column(String(32))
    lastname = Column(String(32))
    email = Column(String(96))
    telephone = Column(String(32))
    total = Column(Float)
    date_added = Column(DateTime, default=func.now())
    order_status_id = Column(Integer)

class OrderProduct(Base):
    __tablename__ = "oc_order_product"
    
    order_product_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("oc_order.order_id"))
    product_id = Column(Integer, ForeignKey("oc_product.product_id"))
    name = Column(String(255))
    quantity = Column(Integer)
    price = Column(Float)
    total = Column(Float)
