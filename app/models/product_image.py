from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base

class ProductImage(Base):
    __tablename__ = "oc_product_image"
    
    product_image_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("oc_product.product_id"))
    image = Column(String(255))
    sort_order = Column(Integer, default=0)