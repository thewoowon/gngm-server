from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewBase(BaseModel):
    title: Optional[str] = None
    contents: Optional[str] = None
    score: Optional[float] = None


class ReviewCreate(ReviewBase):
    store_id: int


class ReviewUpdate(BaseModel):
    title: Optional[str] = None
    contents: Optional[str] = None
    score: Optional[float] = None


class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
