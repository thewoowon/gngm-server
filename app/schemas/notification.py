from pydantic import BaseModel
from datetime import datetime


class NotificationBase(BaseModel):
    title: str
    contents: str
    notification_type: str
    status: str


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    status: str


class NotificationResponse(NotificationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
