from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base


class Address(Base):
    __tablename__ = "address"
    
    id = Column(Integer, autoincrement=True, index=True, primary_key=True)
    province = Column(String(50))
    city = Column(String(50))
    address = Column(String(255))
    postcode = Column(String(10))
    user_id = Column(ForeignKey("users.id"))
    users = relationship("Users", back_populates="address")
