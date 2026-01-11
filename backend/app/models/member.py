"""의원 모델"""
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.database.database import Base

if TYPE_CHECKING:
    from app.models.district import District
    from app.models.member_committee import MemberCommittee


class Member(Base):
    """의원 테이블"""
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(500), nullable=False)
    party: Mapped[str | None] = mapped_column(String(50), nullable=True)
    district_id: Mapped[int] = mapped_column(Integer, ForeignKey("districts.id"), nullable=False)
    term: Mapped[int] = mapped_column(Integer, default=11)

    # 관계
    district: Mapped["District"] = relationship("District", back_populates="members")
    member_committees: Mapped[list["MemberCommittee"]] = relationship(
        "MemberCommittee", back_populates="member"
    )

    def __repr__(self) -> str:
        return f"<Member(id={self.id}, name={self.name}, party={self.party})>"
