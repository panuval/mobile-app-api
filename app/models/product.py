from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, DECIMAL, Date, SmallInteger, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.database import Base

class OneItems(Base):
    __tablename__ = "one_items"
    
    id = Column(Integer, primary_key=True, index=True)
    oc_id = Column(Integer, index=True)  # OpenCart ID that maps to product_id
    # Add other fields as necessary

class Product(Base):
    __tablename__ = "oc_product"
    
    product_id = Column(Integer, primary_key=True, index=True)
    model = Column(String(64), nullable=False)
    sku = Column(String(64), nullable=False)
    upc = Column(String(12), nullable=False)
    ean = Column(String(14), nullable=False)
    jan = Column(String(13), nullable=False)
    isbn = Column(String(17), nullable=False)
    mpn = Column(String(64), nullable=False)
    location = Column(String(128), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    stock_status_id = Column(Integer, nullable=False)
    image = Column(String(255), nullable=True)
    manufacturer_id = Column(Integer, nullable=False)
    shipping = Column(Boolean, nullable=False, default=True)
    price = Column(DECIMAL(15, 4), nullable=False, default=0.0000)
    # original_price is commented out to prevent SQLAlchemy from including it in queries
    # original_price = Column(DECIMAL(15, 4), nullable=True)
    points = Column(Integer, nullable=False, default=0)
    tax_class_id = Column(Integer, nullable=False)
    date_available = Column(Date, nullable=False)
    weight = Column(DECIMAL(15, 8), nullable=False, default=0.00000000)
    weight_class_id = Column(Integer, nullable=False, default=0)
    length = Column(DECIMAL(15, 8), nullable=False, default=0.00000000)
    width = Column(DECIMAL(15, 8), nullable=False, default=0.00000000)
    height = Column(DECIMAL(15, 8), nullable=False, default=0.00000000)
    length_class_id = Column(Integer, nullable=False, default=0)
    subtract = Column(Boolean, nullable=False, default=True)
    minimum = Column(Integer, nullable=False, default=1)
    sort_order = Column(Integer, nullable=False, default=0)
    status = Column(Boolean, nullable=False, default=False)
    viewed = Column(Integer, nullable=False, default=0)
    date_added = Column(DateTime, nullable=False)
    date_modified = Column(DateTime, nullable=False)
    type = Column(Integer, nullable=False)
    product_type = Column(SmallInteger, nullable=True)
    
    # Relationships
    descriptions = relationship("ProductDescription", backref="product")
    images = relationship("ProductImage", backref="product")
    categories = relationship("ProductToCategory", backref="product")
    # Commenting out until tables exist
    # authors = relationship("ProductAuthor", backref="product")
    # publishers = relationship("ProductPublisher", backref="product")

class ProductDescription(Base):
    __tablename__ = "oc_product_description"
    
    product_id = Column(Integer, ForeignKey("oc_product.product_id"), primary_key=True)
    language_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    tag = Column(Text)
    meta_title = Column(String(255))
    meta_description = Column(String(255))
    meta_keyword = Column(String(255))

