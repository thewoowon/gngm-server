from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


# Review 클래스
class Review(Base):
    __tablename__ = "review"

    title = Column(String, nullable=False)
    contents = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    store_id = Column(Integer, ForeignKey("store.id", ondelete="CASCADE"))

    # 관계 설정
    user = relationship("User")
    store = relationship("Store")
