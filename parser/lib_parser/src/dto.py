from dataclasses import dataclass
from pydantic import BaseModel, Field, field_validator
from datetime import date
from .types import AdsStatus


@dataclass
class FbLibAuthData:
    headers: dict
    cookies: dict
    data: dict
    session_id: str


class FbLibGroupAdsCountRequest(BaseModel):
    group_id: str = Field(max_length=20, min_length=10)
    start_date: date
    ads_status: AdsStatus

    @field_validator('start_date')
    @classmethod
    def check_start_date(cls, v):
        if v > date.today():
            raise ValueError('start_date must be less than today date')
        return v