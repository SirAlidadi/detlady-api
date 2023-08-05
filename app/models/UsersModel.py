from sqlalchemy import Column, Integer, String, Boolean
from app.config.database import Base

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(11), unique=True)
    password = Column(String(255))
    is_active = Column(Boolean(), default=False)
    is_admin = Column(Boolean(), default=False)
