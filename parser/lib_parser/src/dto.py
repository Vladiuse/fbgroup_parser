from dataclasses import dataclass
from pydantic import BaseModel, Field, model_validator
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
    end_date: date
    active_status: AdsStatus

    @model_validator(mode='after')
    def check_start_less_than_end(self):
        if self.start_date > self.end_date:
            raise ValueError('start_date must be more or equal to end_date')
        return self
