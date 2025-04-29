from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func

from app.db.database import Base

class Offer(Base):
    __tablename__ = "oc_offer"
    
    offer_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128))
    discount_type = Column(String(32))
    discount_value = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(Boolean, default=True)
