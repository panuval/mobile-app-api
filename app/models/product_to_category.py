from sqlalchemy import Column, Integer, ForeignKey

from app.db.database import Base

class ProductToCategory(Base):
    __tablename__ = "oc_product_to_category"
    
    product_id = Column(Integer, ForeignKey("oc_product.product_id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("oc_category.category_id"), primary_key=True)