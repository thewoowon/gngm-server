from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


# ServiceCategory 클래스
class ServiceCategory(Base):
    __tablename__ = "service_category"

    code = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<ServiceCategory(code={self.code}, name={self.name})>"
