# app/models/banner.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base

class Banner(Base):
    __tablename__ = "oc_banner"
    
    banner_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    status = Column(Boolean, default=True)
    
    # Relationship to banner images
    images = relationship("BannerImage", back_populates="banner")

class BannerImage(Base):
    __tablename__ = "oc_banner_image"
    
    banner_image_id = Column(Integer, primary_key=True, index=True)
    banner_id = Column(Integer, ForeignKey("oc_banner.banner_id"))
    language_id = Column(Integer)
    title = Column(String(64))
    link = Column(String(255))
    image = Column(String(255))
    sort_order = Column(Integer, default=0)
    
    # Relationship to parent banner
    banner = relationship("Banner", back_populates="images")