from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

from app.db.database import Base

class Campaign(Base):
    __tablename__ = "oc_campaign"
    
    campaign_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(Boolean, default=True)
