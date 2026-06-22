from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LoanCreate(BaseModel):
    user_id: int
    device_id: int


class LoanUpdate(BaseModel):
    status: Optional[str] = None
    return_date: Optional[datetime] = None


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True


class UserBasicInfo(BaseModel):
    id: int
    name: str
    email: str


class DeviceBasicInfo(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str


class LoanDetailResponse(BaseModel):
    loan_id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime] = None
    user: UserBasicInfo
    device: DeviceBasicInfo
