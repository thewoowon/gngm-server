from pydantic import BaseModel
from typing import Optional
from app.models.chat import Chat
from app.schemas.user import UserResponse
from datetime import datetime


class ChatParticipantBase(BaseModel):
    role: str
    joined_at: datetime


class ChatParticipantCreate(ChatParticipantBase):
    pass


class ChatParticipantResponse(ChatParticipantBase):
    id: int

    user: Optional[UserResponse]

    class Config:
        from_attributes = True
