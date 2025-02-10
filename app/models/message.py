from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


# Message 클래스
class Message(Base):
    __tablename__ = "message"

    message = Column(String, nullable=False)
    sender_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))
    chat_id = Column(Integer, ForeignKey("chat.id", ondelete="CASCADE"))

    # 관계 설정
    sender = relationship("User")
    chat = relationship("Chat", back_populates="messages")

    __table_args__ = (
        UniqueConstraint('chat_id', 'id', name='unique_chat_message_id'),
    )
