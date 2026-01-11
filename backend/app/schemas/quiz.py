"""퀴즈 스키마"""
from pydantic import BaseModel

from app.schemas.member import MemberResponse


class QuizQuestionResponse(BaseModel):
    """퀴즈 문제 응답 스키마"""

    answer: MemberResponse
    options: list[MemberResponse]


class QuizResultResponse(BaseModel):
    """퀴즈 결과 응답 스키마"""

    total_questions: int
    correct_answers: int
    accuracy: float  # 0-100
