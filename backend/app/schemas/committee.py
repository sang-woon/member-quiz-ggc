"""위원회 스키마"""
from pydantic import BaseModel


class CommitteeBase(BaseModel):
    """위원회 기본 스키마"""

    name: str


class CommitteeResponse(CommitteeBase):
    """위원회 응답 스키마"""

    id: int

    class Config:
        from_attributes = True
