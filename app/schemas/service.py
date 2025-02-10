from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.service_category import ServiceCategoryResponse


class ServiceBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[int] = None
    discount_rate: Optional[int] = None
    is_representative: Optional[int] = None
    representative_image: Optional[str] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    service_category: Optional[ServiceCategoryResponse] = None

    class Config:
        from_attributes = True
