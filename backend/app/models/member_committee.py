"""의원-위원회 연결 모델"""
from sqlalchemy import Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.database.database import Base

if TYPE_CHECKING:
    from app.models.member import Member
    from app.models.committee import Committee


class MemberCommittee(Base):
    """의원-위원회 연결 테이블"""
    __tablename__ = "member_committees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(Integer, ForeignKey("members.id"), nullable=False)
    committee_id: Mapped[int] = mapped_column(Integer, ForeignKey("committees.id"), nullable=False)
    is_chairman: Mapped[bool] = mapped_column(Boolean, default=False)

    # 관계
    member: Mapped["Member"] = relationship("Member", back_populates="member_committees")
    committee: Mapped["Committee"] = relationship("Committee", back_populates="member_committees")

    def __repr__(self) -> str:
        return f"<MemberCommittee(member_id={self.member_id}, committee_id={self.committee_id})>"
