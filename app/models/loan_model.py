from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    loan_date = Column(DateTime, server_default=func.now())
    return_date = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="active")
    #forein keys
    user = relationship("User", back_populates="loans")
    device = relationship("Device", back_populates="loans")