"""의원 API 라우터"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import math

from app.database.database import get_db
from app.services.member_service import get_members, get_member_by_id, get_member_committees
from app.schemas import (
    MemberResponse,
    MemberDetailResponse,
    PaginationMeta,
    CommitteeResponse,
)

router = APIRouter(prefix="/api/members", tags=["members"])


@router.get("")
def list_members(
    district_id: Optional[int] = Query(None, alias="districtId"),
    committee_id: Optional[int] = Query(None, alias="committeeId"),
    party: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """의원 목록 조회"""
    members, total = get_members(
        db,
        district_id=district_id,
        committee_id=committee_id,
        party=party,
        page=page,
        size=size,
    )

    data = [
        {
            "id": m.id,
            "name": m.name,
            "photoUrl": m.photo_url,
            "party": m.party,
            "districtId": m.district_id,
            "districtName": m.district.name if m.district else "",
            "term": m.term,
        }
        for m in members
    ]

    return {
        "data": data,
        "meta": {
            "total": total,
            "page": page,
            "size": size,
            "totalPages": math.ceil(total / size) if total > 0 else 1,
        },
    }


@router.get("/{member_id}")
def get_member(member_id: int, db: Session = Depends(get_db)):
    """의원 상세 조회"""
    member = get_member_by_id(db, member_id)

    if not member:
        raise HTTPException(status_code=404, detail="의원을 찾을 수 없습니다.")

    committees = get_member_committees(member)

    return {
        "data": {
            "id": member.id,
            "name": member.name,
            "photoUrl": member.photo_url,
            "party": member.party,
            "districtId": member.district_id,
            "districtName": member.district.name if member.district else "",
            "term": member.term,
            "committees": [
                {"id": c.id, "name": c.name}
                for c in committees
            ],
        }
    }
