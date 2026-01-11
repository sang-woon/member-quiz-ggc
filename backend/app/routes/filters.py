"""필터 API 라우터"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models import District, Committee

router = APIRouter(prefix="/api", tags=["filters"])


@router.get("/districts")
def get_districts(db: Session = Depends(get_db)):
    """지역구 목록 조회"""
    districts = db.query(District).order_by(District.name).all()

    return {
        "data": [
            {
                "id": d.id,
                "name": d.name,
                "region": d.region,
            }
            for d in districts
        ]
    }


@router.get("/committees")
def get_committees(db: Session = Depends(get_db)):
    """위원회 목록 조회"""
    committees = db.query(Committee).order_by(Committee.name).all()

    return {
        "data": [
            {
                "id": c.id,
                "name": c.name,
            }
            for c in committees
        ]
    }
