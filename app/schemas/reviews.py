from fastapi import HTTPException, status
from pydantic import BaseModel, validator


class ReviewParams(BaseModel):
    rating: int

    @validator("rating")
    def validate_average_rating(cls, v):
        if v is not None:
            if not (1 <= v <= 5):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="rating must be between 1 and 5",
                )
        return v
