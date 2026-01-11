"""스키마 패키지"""
from app.schemas.common import PaginationMeta, ApiResponse, ApiListResponse
from app.schemas.district import DistrictBase, DistrictResponse
from app.schemas.committee import CommitteeBase, CommitteeResponse
from app.schemas.member import MemberBase, MemberResponse, MemberDetailResponse
from app.schemas.quiz import QuizQuestionResponse, QuizResultResponse

__all__ = [
    # Common
    "PaginationMeta",
    "ApiResponse",
    "ApiListResponse",
    # District
    "DistrictBase",
    "DistrictResponse",
    # Committee
    "CommitteeBase",
    "CommitteeResponse",
    # Member
    "MemberBase",
    "MemberResponse",
    "MemberDetailResponse",
    # Quiz
    "QuizQuestionResponse",
    "QuizResultResponse",
]
