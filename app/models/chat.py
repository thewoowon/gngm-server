from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


# Chat 클래스
class Chat(Base):
    __tablename__ = "chat"

    # 전달을 처음 생성하면 해당 채팅은 단체 채팅으로 생성됨
    founder_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))
    article_id = Column(Integer, ForeignKey("article.id", ondelete="CASCADE"))

    # 관계 설정: foreign_keys에 실제 컬럼 객체 사용
    founder = relationship(
        "User",
        back_populates="created_chats",
        foreign_keys=[founder_id]  # 문자열이 아닌 컬럼 객체
    )

    article = relationship("Article", back_populates="chat")

    participants = relationship(
        "ChatParticipant", back_populates="chat", cascade="all, delete-orphan"
    )
    messages = relationship(
        "Message", back_populates="chat", cascade="all, delete")
