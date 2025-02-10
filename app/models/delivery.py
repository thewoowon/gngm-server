from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


# Delivery 클래스
class Delivery(Base):
    __tablename__ = "delivery"

    request_date = Column(String, nullable=False)
    request_time = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    article_id = Column(Integer, ForeignKey("article.id", ondelete="CASCADE"))
    order_id = Column(Integer, ForeignKey("order.id", ondelete="CASCADE"))

    # 관계 설정
    user = relationship("User")
    article = relationship("Article", back_populates="deliveries")
    order = relationship("Order", back_populates="deliveries")

    __table_args__ = (
        UniqueConstraint('user_id', 'article_id', name='unique_delivery'),
    )
