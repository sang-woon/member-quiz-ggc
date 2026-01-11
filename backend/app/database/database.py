"""데이터베이스 설정"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 환경변수에서 DATABASE_URL 읽기 (Supabase PostgreSQL)
# 로컬 개발시에는 SQLite 사용
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Supabase PostgreSQL (프로덕션)
    # Supabase URL이 postgres://로 시작하면 postgresql://로 변경
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
else:
    # SQLite (로컬 개발)
    SQLALCHEMY_DATABASE_URL = "sqlite:///./members.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """SQLAlchemy Base 클래스"""
    pass


def get_db():
    """데이터베이스 세션 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """테이블 생성"""
    Base.metadata.create_all(bind=engine)
