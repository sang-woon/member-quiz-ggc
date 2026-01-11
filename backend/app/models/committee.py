"""위원회 모델"""
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.database.database import Base

if TYPE_CHECKING:
    from app.models.member_committee import MemberCommittee


class Committee(Base):
    """위원회 테이블"""
    __tablename__ = "committees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # 관계
    member_committees: Mapped[list["MemberCommittee"]] = relationship(
        "MemberCommittee", back_populates="committee"
    )

    def __repr__(self) -> str:
        return f"<Committee(id={self.id}, name={self.name})>"
