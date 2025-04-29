from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.database import Base

class Cart(Base):
    __tablename__ = "oc_cart"
    
    cart_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    session_id = Column(String(32))

class CartItem(Base):
    __tablename__ = "oc_cart_item"
    
    cart_item_id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("oc_cart.cart_id"))
    customer_id = Column(Integer)
    product_id = Column(Integer, ForeignKey("oc_product.product_id"))
    quantity = Column(Integer)