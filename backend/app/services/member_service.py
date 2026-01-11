"""의원 서비스"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional

from app.models import Member, District, Committee, MemberCommittee


def get_members(
    db: Session,
    district_id: Optional[int] = None,
    committee_id: Optional[int] = None,
    party: Optional[str] = None,
    page: int = 1,
    size: int = 20,
) -> tuple[list[Member], int]:
    """의원 목록 조회 (필터링, 페이지네이션)"""
    query = db.query(Member).options(joinedload(Member.district))

    # 지역구 필터
    if district_id:
        query = query.filter(Member.district_id == district_id)

    # 위원회 필터
    if committee_id:
        member_ids = (
            db.query(MemberCommittee.member_id)
            .filter(MemberCommittee.committee_id == committee_id)
            .subquery()
        )
        query = query.filter(Member.id.in_(member_ids))

    # 정당 필터
    if party:
        query = query.filter(Member.party == party)

    # 전체 개수
    total = query.count()

    # 페이지네이션
    offset = (page - 1) * size
    members = query.offset(offset).limit(size).all()

    return members, total


def get_member_by_id(db: Session, member_id: int) -> Optional[Member]:
    """의원 상세 조회"""
    return (
        db.query(Member)
        .options(
            joinedload(Member.district),
            joinedload(Member.member_committees).joinedload(MemberCommittee.committee),
        )
        .filter(Member.id == member_id)
        .first()
    )


def get_member_committees(member: Member) -> list[Committee]:
    """의원의 위원회 목록 조회"""
    return [mc.committee for mc in member.member_committees]
