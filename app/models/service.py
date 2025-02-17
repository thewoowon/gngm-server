from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


# Service 클래스
class Service(Base):
    __tablename__ = "service"

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    discount_rate = Column(Integer, nullable=False)
    # 대표 서비스 여부
    is_representative = Column(Integer, nullable=False, default=0)
    # 대표 이미지
    representative_image = Column(String, nullable=True)
    store_id = Column(Integer, ForeignKey("store.id", ondelete="CASCADE"))
    service_category_id = Column(Integer, ForeignKey("service_category.id"))

    # 관계 설정
    store = relationship("Store", back_populates="services")
    service_category = relationship("ServiceCategory")
    orders = relationship("Order", back_populates="service")

    def __repr__(self):
        return f"<Service(name={self.name}, description={self.description}, unit={self.unit}, price={self.price}, discount_rate={self.discount_rate}, is_representative={self.is_representative})>"
