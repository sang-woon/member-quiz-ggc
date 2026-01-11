"""지역구 모델"""
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.database.database import Base

if TYPE_CHECKING:
    from app.models.member import Member


class District(Base):
    """지역구 테이블"""
    __tablename__ = "districts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    region: Mapped[str] = mapped_column(String(50), nullable=False)

    # 관계
    members: Mapped[list["Member"]] = relationship("Member", back_populates="district")

    def __repr__(self) -> str:
        return f"<District(id={self.id}, name={self.name}, region={self.region})>"
