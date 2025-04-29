from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base

class LayoutSection(Base):
    """
    Model representing a section in the home page layout.
    """
    __tablename__ = "oc_layout_section"
    
    section_id = Column(Integer, primary_key=True, index=True)
    display_type = Column(String(20), nullable=False)  # TEXT, CAROUSEL, TILE
    content_type = Column(String(20), nullable=False)  # BANNER, BOOK, CATEGORY, AUTHOR, PUBLISHER
    title = Column(String(255), nullable=True)
    show_title = Column(Boolean, default=True)
    show_view_all = Column(Boolean, default=False)
    order_sort = Column(Integer, nullable=False)
    visible = Column(Boolean, default=True)
    date_added = Column(DateTime, default=func.now())
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now())

class LayoutSectionContent(Base):
    """
    Model representing content items for a section.
    """
    __tablename__ = "oc_layout_section_content"
    
    content_id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("oc_layout_section.section_id"))
    reference_id = Column(Integer, nullable=False)  # ID of the referenced item (product, category, etc.)
    reference_type = Column(String(20), nullable=False)  # PRODUCT, CATEGORY, AUTHOR, PUBLISHER, BANNER
    order_sort = Column(Integer, nullable=False)
    visible = Column(Boolean, default=True)