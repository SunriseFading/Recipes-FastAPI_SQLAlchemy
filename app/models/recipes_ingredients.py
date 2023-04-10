from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer


class RecipeIngredient(Base):
    __tablename__ = "recipes_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True, index=True)
    ingredient_id = Column(
        Integer, ForeignKey("ingredients.id"), primary_key=True, index=True
    )
