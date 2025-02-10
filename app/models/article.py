from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


# Article 클래스
class Article(Base):
    __tablename__ = "article"

    title = Column(String, nullable=False)  # 제목
    contents = Column(String, nullable=False)  # 내용
    article_type = Column(String, nullable=False)  # 게시글 타입
    pick_up_location = Column(String, nullable=False)  # 희망장소
    # 희망 수령 일자 yyyyMMdd-yyyyMMdd, 단, 출발일자 보다 클 수 없음
    pick_up_date = Column(String, nullable=False)
    # 희망 수령 시간대 HH:mm-HH:mm
    pick_up_time = Column(String, nullable=False)
    destination = Column(String, nullable=False)  # 목적지
    departure_date = Column(
        String, nullable=False)  # 출발날짜 yyyyMMdd
    number_of_recruits = Column(Integer, nullable=False)  # 모집인원
    process_status = Column(String, nullable=False)  # 처리상태
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))

    # 관계 설정
    user = relationship("User", back_populates="articles")
    address = relationship("Address", uselist=False, back_populates="article")
    deliveries = relationship("Delivery", back_populates="article")
    # 아티클 하나당 채팅방은 하나, back_populates 불필요
    chat = relationship("Chat", uselist=False, back_populates="article")

    def __repr__(self):
        return f"<Article(title={self.title}, contents={self.contents}, article_type={self.article_type}, pick_up_location={self.pick_up_location}, pick_up_date={self.pick_up_date}, pick_up_time={self.pick_up_time}, destination={self.destination}, departure_date={self.departure_date}, number_of_recruits={self.number_of_recruits}, process_status={self.process_status})>"
