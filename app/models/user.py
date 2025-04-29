from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.database import Base

class User(Base):
    __tablename__ = "oc_user"
    
    user_id = Column(Integer, primary_key=True, index=True)
    user_group_id = Column(Integer)
    username = Column(String(20))
    password = Column(String(40))
    salt = Column(String(9))
    firstname = Column(String(32))
    lastname = Column(String(32))
    email = Column(String(96))
    image = Column(String(255))
    code = Column(String(40))
    ip = Column(String(40))
    status = Column(Boolean)
    date_added = Column(DateTime)