"""퀴즈 API 라우터"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database.database import get_db
from app.services.quiz_service import generate_quiz_question

router = APIRouter(prefix="/api/quiz", tags=["quiz"])


@router.get("")
def get_quiz_question(
    district_id: Optional[int] = Query(None, alias="districtId"),
    committee_id: Optional[int] = Query(None, alias="committeeId"),
    db: Session = Depends(get_db),
):
    """퀴즈 문제 생성"""
    try:
        question = generate_quiz_question(
            db,
            district_id=district_id,
            committee_id=committee_id,
        )
        return question
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
