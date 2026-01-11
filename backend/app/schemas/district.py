"""지역구 스키마"""
from pydantic import BaseModel


class DistrictBase(BaseModel):
    """지역구 기본 스키마"""

    name: str
    region: str


class DistrictResponse(DistrictBase):
    """지역구 응답 스키마"""

    id: int

    class Config:
        from_attributes = True
