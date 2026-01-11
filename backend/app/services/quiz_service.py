"""퀴즈 서비스"""
import random
from sqlalchemy.orm import Session, joinedload
from typing import Optional

from app.models import Member, MemberCommittee


def generate_quiz_question(
    db: Session,
    district_id: Optional[int] = None,
    committee_id: Optional[int] = None,
) -> dict:
    """퀴즈 문제 생성 (4지선다)"""
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

    members = query.all()

    # 최소 4명이 필요
    if len(members) < 4:
        # 필터 조건이 맞는 의원이 4명 미만이면 전체에서 보충
        all_members = db.query(Member).options(joinedload(Member.district)).all()
        if len(all_members) < 4:
            raise ValueError("퀴즈를 생성할 수 있는 의원 수가 충분하지 않습니다.")
        members = all_members

    # 랜덤하게 4명 선택
    selected = random.sample(members, 4)

    # 첫 번째가 정답
    answer = selected[0]

    # 보기 섞기
    options = selected.copy()
    random.shuffle(options)

    return {
        "answer": _member_to_dict(answer),
        "options": [_member_to_dict(m) for m in options],
    }


def _member_to_dict(member: Member) -> dict:
    """Member 객체를 딕셔너리로 변환"""
    return {
        "id": member.id,
        "name": member.name,
        "photoUrl": member.photo_url,
        "party": member.party,
        "districtId": member.district_id,
        "districtName": member.district.name if member.district else "",
        "term": member.term,
    }
