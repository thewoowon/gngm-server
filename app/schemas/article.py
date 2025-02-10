from pydantic import BaseModel
from typing import Optional
from app.schemas.address import AddressBase
from app.schemas.delivery import DeliveryBase
from app.schemas.message import MessageResponse
from app.schemas.user import UserResponse
from app.schemas.chat import ChatResponse


class ArticleBase(BaseModel):
    title: str
    contents: str
    article_type: str
    pick_up_location: str
    pick_up_date: str
    pick_up_time: str
    destination: str
    departure_date: str
    number_of_recruits: int
    process_status: str


# access_token으로 user_id를 찾기 위한 클래스
class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    contents: Optional[str] = None
    article_type: Optional[str] = None
    pick_up_location: Optional[str] = None
    pick_up_date: Optional[str] = None
    pick_up_time: Optional[str] = None
    destination: Optional[str] = None
    departure_date: Optional[str] = None
    number_of_recruits: Optional[int] = None
    process_status: Optional[str] = None


class ArticleResponse(ArticleBase):
    id: int
    address: Optional[AddressBase]
    deliveries: Optional[list[DeliveryBase]] = []
    user: Optional[UserResponse]
    chat: Optional[ChatResponse]
    messages: Optional[list[MessageResponse]] = []

    class Config:
        from_attributes = True
