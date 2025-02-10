from pydantic import BaseModel
from typing import Optional
from app.schemas.chat_participant import ChatParticipantResponse
from app.schemas.user import UserResponse


class ChatBase(BaseModel):
    pass


class ChatCreate(ChatBase):
    pass


class ChatResponse(ChatBase):
    id: int

    # founder: Optional[UserResponse]
    # participants: Optional[list[ChatParticipantResponse]]
    # messages: Optional[list[MessageResponse]]

    class Config:
        from_attributes = True

class ChatMainResponse(ChatBase):
    id: int

    founder: Optional[UserResponse]
    participants: Optional[list[ChatParticipantResponse]]
    # messages: Optional[list[MessageResponse]]

    class Config:
        from_attributes = True
