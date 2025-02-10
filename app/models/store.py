from sqlalchemy import Column, String, Integer, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship


# Store 클래스
class Store(Base):
    __tablename__ = "store"

    name = Column(String, index=True)
    address = Column(String, nullable=False)
    store_type = Column(String, nullable=False)
    business_hours = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    # 대표 이미지
    representative_image = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    # 관계 설정
    user = relationship("User", back_populates="stores")
    orders = relationship("Order", back_populates="store")
    services = relationship("Service", back_populates="store")

    def __repr__(self):
        return f"<Store(name={self.name}, address={self.address}, store_type={self.store_type}, business_hours={self.business_hours}, phone_number={self.phone_number})>"
