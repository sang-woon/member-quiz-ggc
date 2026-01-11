"""Vercel Serverless Function 엔트리포인트"""
import sys
from pathlib import Path

# backend 폴더를 모듈 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.main import app

# Vercel에서 FastAPI 앱을 ASGI로 실행
handler = app
