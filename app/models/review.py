from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.sql import func

from app.db.database import Base

class Review(Base):
    __tablename__ = "oc_review"
    
    review_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    customer_id = Column(Integer)
    customer_name = Column(String(64))
    rating = Column(Integer)
    comment = Column(Text)
    status = Column(Boolean, default=True)
