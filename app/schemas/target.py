from typing import Optional
from pydantic import BaseModel, Field


class TargetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)


class TargetCreate(TargetBase):
    notes: str = Field(default="", max_length=5000)


class TargetUpdate(BaseModel):
    notes: Optional[str] = Field(None, max_length=5000)
    complete: Optional[bool] = None


class TargetResponse(TargetBase):
    id: int
    mission_id: int
    notes: str
    complete: bool

    class Config:
        from_attributes = True

