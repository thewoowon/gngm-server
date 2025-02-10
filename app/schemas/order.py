from pydantic import BaseModel
from typing import Optional
from app.schemas.store import StoreBase
from datetime import datetime


class OrderBase(BaseModel):
    description: str
    order_type: str


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    description: Optional[str] = None
    order_type: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    store: Optional[StoreBase] = None

    class Config:
        from_attributes = True
