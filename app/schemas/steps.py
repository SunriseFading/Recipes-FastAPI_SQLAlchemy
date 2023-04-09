from fastapi import HTTPException, status
from pydantic import BaseModel, validator


class Step(BaseModel):
    name: str
    time: int
    description: str | None = None

    @validator("time")
    def validate_average_rating(cls, v):
        if v < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="time must be greater or equal 0",
            )
        return v


class StepResponse(BaseModel):
    id: int
    name: str
    time: int
    description: str | None

    class Config:
        orm_mode = True
