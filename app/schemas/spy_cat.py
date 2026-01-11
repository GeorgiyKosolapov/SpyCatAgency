from pydantic import BaseModel, Field


class SpyCatBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    years_of_experience: int = Field(..., ge=0)
    breed: str = Field(..., min_length=1, max_length=100)
    salary: float = Field(..., gt=0)


class SpyCatCreate(SpyCatBase):
    pass


class SpyCatUpdate(BaseModel):
    salary: float = Field(..., gt=0)


class SpyCatResponse(SpyCatBase):
    id: int

    class Config:
        from_attributes = True

