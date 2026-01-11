"""의원얼굴퀴즈 API 서버"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="의원얼굴퀴즈 API",
    description="경기도의회 11대 의원 얼굴 학습 퀴즈 API",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """헬스 체크"""
    return {"message": "의원얼굴퀴즈 API", "status": "running"}


@app.get("/api/health")
async def health_check():
    """API 헬스 체크"""
    return {"status": "healthy"}


# TODO: 라우터 등록
# from app.routes import members, quiz, filters
# app.include_router(members.router)
# app.include_router(quiz.router)
# app.include_router(filters.router)
