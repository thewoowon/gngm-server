from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeliveryBase(BaseModel):
    request_date: str
    request_time: str
    user_id: int
    article_id: int


class DeliveryCreate(DeliveryBase):
    pass


class DeliveryUpdate(BaseModel):
    request_date: Optional[str] = None
    request_time: Optional[str] = None


class DeliveryResponse(DeliveryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
