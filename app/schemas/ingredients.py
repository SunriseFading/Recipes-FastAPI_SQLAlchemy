from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str


class IngredientResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
