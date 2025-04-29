from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base

class Publisher(Base):
    __tablename__ = "oc_publisher"
    
    publisher_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    image = Column(String(255))
    status = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

class ProductPublisher(Base):
    __tablename__ = "oc_product_publisher"
    
    product_id = Column(Integer, ForeignKey("oc_product.product_id"), primary_key=True)
    publisher_id = Column(Integer, ForeignKey("oc_publisher.publisher_id"), primary_key=True)