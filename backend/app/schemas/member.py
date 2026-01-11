"""의원 스키마"""
from pydantic import BaseModel, Field, computed_field
from typing import Optional

from app.schemas.committee import CommitteeResponse


class MemberBase(BaseModel):
    """의원 기본 스키마"""

    name: str
    photo_url: str = Field(alias="photoUrl", serialization_alias="photoUrl")
    party: Optional[str] = None
    district_id: int = Field(alias="districtId", serialization_alias="districtId")
    term: int = 11


class MemberResponse(MemberBase):
    """의원 응답 스키마"""

    id: int
    district_name: str = Field(alias="districtName", serialization_alias="districtName")

    class Config:
        from_attributes = True
        populate_by_name = True


class MemberDetailResponse(MemberResponse):
    """의원 상세 응답 스키마 (위원회 포함)"""

    committees: list[CommitteeResponse] = []

    class Config:
        from_attributes = True
        populate_by_name = True
