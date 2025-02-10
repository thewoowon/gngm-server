from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.user import UserResponse


class MessageBase(BaseModel):
    message: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    message: str


class MessageResponse(MessageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    sender: Optional[UserResponse]

    class Config:
        from_attributes = True
