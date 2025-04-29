from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.database import Base

class Category(Base):
    __tablename__ = "oc_category"
    
    category_id = Column(Integer, primary_key=True, index=True)
    image = Column(String(255), nullable=True)
    parent_id = Column(Integer, nullable=False, default=0, primary_key=True)
    top = Column(Boolean, nullable=False)
    column = Column(Integer, nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
    status = Column(Boolean, nullable=False)
    date_added = Column(DateTime, nullable=False)
    date_modified = Column(DateTime, nullable=False)
    
    # Relationships
    descriptions = relationship("CategoryDescription", backref="category")

class CategoryDescription(Base):
    __tablename__ = "oc_category_description"
    
    category_id = Column(Integer, ForeignKey("oc_category.category_id"), primary_key=True)
    language_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    meta_title = Column(String(255))
    meta_description = Column(String(255))
    meta_keyword = Column(String(255))