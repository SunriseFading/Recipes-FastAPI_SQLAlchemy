from app.models.recipes import fields
from app.schemas.ingredients import Ingredient, IngredientResponse
from app.schemas.steps import Step, StepResponse
from fastapi import HTTPException, status
from pydantic import BaseModel, validator


class Recipe(BaseModel):
    name: str
    description: str | None = None
    ingredients: list[Ingredient]
    steps: list[Step]


class RecipeResponse(BaseModel):
    id: int
    name: str
    average_rating: float | None
    total_time: int
    ingredients: list[IngredientResponse]
    description: str
    steps: list[StepResponse]

    class Config:
        orm_mode = True


class RecipeParams(BaseModel):
    order_by: str | None = None
    average_rating: float | None = None

    @validator("order_by")
    def validate_order_by(cls, v):
        if v is not None:
            if v[1:] not in fields and v not in fields:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"recipe model didn't have {v} field",
                )
        return v

    @validator("average_rating")
    def validate_average_rating(cls, v):
        if v is not None:
            if not (1 <= v <= 5):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="average_rating must be between 1 and 5",
                )
        return v
