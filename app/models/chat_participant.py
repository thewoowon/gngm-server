from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

# ChatParticipant 클래스 (중간 테이블)


class ChatParticipant(Base):
    __tablename__ = "chat_participant"

    chat_id = Column(Integer, ForeignKey("chat.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    # 예: "founder", "moderator", "participant"
    role = Column(String, nullable=False, default="participant")
    joined_at = Column(DateTime, server_default=func.now())  # 참가 시간

    # 관계 설정
    chat = relationship("Chat", back_populates="participants")
    user = relationship("User", back_populates="chat_participations")

    __table_args__ = (
        UniqueConstraint('chat_id', 'user_id', name='unique_chat_participant'),
    )
