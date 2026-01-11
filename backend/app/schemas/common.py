"""공통 스키마"""
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class PaginationMeta(BaseModel):
    """페이지네이션 메타 정보"""

    total: int
    page: int
    size: int
    total_pages: int


class ApiResponse(BaseModel, Generic[T]):
    """단일 항목 API 응답"""

    data: T


class ApiListResponse(BaseModel, Generic[T]):
    """목록 API 응답"""

    data: list[T]
    meta: PaginationMeta
