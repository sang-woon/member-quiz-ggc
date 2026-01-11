"""의원얼굴퀴즈 API 서버"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 모델 임포트 (테이블 등록)
from app.models import District, Committee, Member, MemberCommittee  # noqa: F401
from app.database.database import create_tables
from app.routes import members_router, quiz_router, filters_router

app = FastAPI(
    title="의원얼굴퀴즈 API",
    description="경기도의회 11대 의원 얼굴 학습 퀴즈 API",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """앱 시작 시 테이블 생성"""
    create_tables()


@app.get("/")
async def root():
    """헬스 체크"""
    return {"message": "의원얼굴퀴즈 API", "status": "running"}


@app.get("/api/health")
async def health_check():
    """API 헬스 체크"""
    return {"status": "healthy"}


# 라우터 등록
app.include_router(members_router)
app.include_router(quiz_router)
app.include_router(filters_router)
