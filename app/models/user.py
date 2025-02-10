from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.models.chat import Chat


# User 클래스 -> 대부분 모든 객체가 User 클래스를 사용
class User(Base):
    __tablename__ = "user"

    # 일반 필드
    name = Column(String, nullable=False)  # 이름
    nickname = Column(String, nullable=True)  # 닉네임
    email = Column(String, unique=True, index=True, nullable=False)  # 이메일
    phone_number = Column(String, nullable=False)  # 전화번호
    address = Column(String, nullable=True)  # 주소
    src = Column(String, nullable=True)  # 프로필 사진
    is_auto_login = Column(Integer, nullable=False, default=0)  # 자동 로그인 여부
    accident_date = Column(DateTime, default=func.now(),
                           nullable=False)  # 사고 날짜
    job = Column(String, nullable=True)  # 직업
    job_description = Column(String, nullable=True)  # 직업 설명
    is_job_open = Column(Integer, nullable=False, default=0)  # 직업 공개 여부
    is_admin = Column(Integer, nullable=False, default=0)  # 관리자 여부
    is_deleted = Column(Integer, nullable=False, default=0)  # 삭제 여부
    # 사용자 타입 (0: 일반 사용자, 1: 카카오 사용자, 2: 네이버 사용자, 3: 구글 사용자)
    user_type = Column(Integer, nullable=False, default=0)
    # 사용자 상태 (0: 정상, 1: 휴면, 2: 정지)
    status = Column(Integer, nullable=False, default=0)
    # 판매자 여부인지 확인하는 필드 (0: 구매자, 1: 판매자)
    is_seller = Column(Integer, nullable=False, default=0)

    # 관계 설정
    stores = relationship("Store", back_populates="user")
    orders = relationship("Order", back_populates="user")
    articles = relationship("Article", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    tokens = relationship("Token", back_populates="user")

    # User가 생성한 채팅방 (founder)
    created_chats = relationship(
        "Chat",
        back_populates="founder",
        foreign_keys=[Chat.founder_id]  # 문자열이 아닌 컬럼 객체
    )

    # User가 참여한 채팅방 (attendant)
    chat_participations = relationship(
        "ChatParticipant", back_populates="user", cascade="all, delete-orphan"
    )
