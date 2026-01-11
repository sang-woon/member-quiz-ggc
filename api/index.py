"""Vercel Serverless Function - 의원얼굴퀴즈 API"""
import os
import random
import math
from typing import Optional

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None


class Base(DeclarativeBase):
    pass


# Models
class District(Base):
    __tablename__ = "districts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    region: Mapped[str | None] = mapped_column(String(50), nullable=True)
    members: Mapped[list["Member"]] = relationship("Member", back_populates="district")


class Committee(Base):
    __tablename__ = "committees"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


class Member(Base):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(500), nullable=False)
    party: Mapped[str | None] = mapped_column(String(50), nullable=True)
    district_id: Mapped[int] = mapped_column(Integer, ForeignKey("districts.id"), nullable=False)
    term: Mapped[int] = mapped_column(Integer, default=11)
    district: Mapped["District"] = relationship("District", back_populates="members")


class MemberCommittee(Base):
    __tablename__ = "member_committees"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(Integer, ForeignKey("members.id"))
    committee_id: Mapped[int] = mapped_column(Integer, ForeignKey("committees.id"))


# FastAPI app
app = FastAPI(title="의원얼굴퀴즈 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    if not SessionLocal:
        raise HTTPException(status_code=500, detail="Database not configured")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api")
def root():
    return {"message": "의원얼굴퀴즈 API", "status": "running"}


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.get("/api/members")
def list_members(
    district_id: Optional[int] = Query(None, alias="districtId"),
    committee_id: Optional[int] = Query(None, alias="committeeId"),
    party: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    db = next(get_db())
    try:
        query = db.query(Member)

        if district_id:
            query = query.filter(Member.district_id == district_id)
        if party:
            query = query.filter(Member.party == party)
        if committee_id:
            query = query.join(MemberCommittee).filter(MemberCommittee.committee_id == committee_id)

        total = query.count()
        members = query.offset((page - 1) * size).limit(size).all()

        return {
            "data": [
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
            ],
            "meta": {
                "total": total,
                "page": page,
                "size": size,
                "totalPages": math.ceil(total / size) if total > 0 else 1,
            },
        }
    finally:
        db.close()


@app.get("/api/quiz")
def get_quiz(
    district_id: Optional[int] = Query(None, alias="districtId"),
    committee_id: Optional[int] = Query(None, alias="committeeId"),
):
    db = next(get_db())
    try:
        query = db.query(Member)

        if district_id:
            query = query.filter(Member.district_id == district_id)
        if committee_id:
            query = query.join(MemberCommittee).filter(MemberCommittee.committee_id == committee_id)

        members = query.all()

        if len(members) < 4:
            all_members = db.query(Member).all()
            members = list(set(members + random.sample(all_members, min(4, len(all_members)))))

        if len(members) < 4:
            raise HTTPException(status_code=400, detail="문제를 생성할 충분한 의원이 없습니다")

        answer = random.choice(members)
        wrong_options = [m for m in members if m.id != answer.id]
        options = random.sample(wrong_options, min(3, len(wrong_options)))
        options.append(answer)
        random.shuffle(options)

        def member_to_dict(m):
            return {
                "id": m.id,
                "name": m.name,
                "photoUrl": m.photo_url,
                "party": m.party,
                "districtId": m.district_id,
                "districtName": m.district.name if m.district else "",
                "term": m.term,
            }

        return {
            "answer": member_to_dict(answer),
            "options": [member_to_dict(o) for o in options],
        }
    finally:
        db.close()


@app.get("/api/districts")
def get_districts():
    db = next(get_db())
    try:
        districts = db.query(District).order_by(District.name).all()
        return {
            "data": [{"id": d.id, "name": d.name, "region": d.region} for d in districts]
        }
    finally:
        db.close()


@app.get("/api/committees")
def get_committees():
    db = next(get_db())
    try:
        committees = db.query(Committee).order_by(Committee.name).all()
        return {
            "data": [{"id": c.id, "name": c.name} for c in committees]
        }
    finally:
        db.close()
