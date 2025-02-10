from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.service import ServiceResponse
from typing import List


class StoreBase(BaseModel):
    name: str
    address: Optional[str] = None
    store_type: Optional[str] = None
    business_hours: Optional[str] = None
    phone_number: Optional[str] = None
    representative_image: Optional[str] = None


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    store_type: Optional[str] = None
    business_hours: Optional[str] = None
    phone_number: Optional[str] = None


class StoreResponse(StoreBase):
    id: int
    created_at: datetime
    updated_at: datetime
    # services: Optional[List[ServiceResponse]] = None
    services: Optional[List[ServiceResponse]] = None

    class Config:
        from_attributes = True
