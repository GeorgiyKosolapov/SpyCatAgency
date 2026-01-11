from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

from app.schemas.target import TargetCreate, TargetResponse


class MissionCreate(BaseModel):
    cat_id: Optional[int] = None
    targets: List[TargetCreate] = Field(..., min_length=1, max_length=3)

    @field_validator('targets')
    @classmethod
    def validate_targets_count(cls, v):
        if len(v) < 1 or len(v) > 3:
            raise ValueError('Mission must have between 1 and 3 targets')
        return v


class MissionAssign(BaseModel):
    cat_id: int


class MissionResponse(BaseModel):
    id: int
    cat_id: Optional[int]
    complete: bool
    targets: List[TargetResponse]

    class Config:
        from_attributes = True

