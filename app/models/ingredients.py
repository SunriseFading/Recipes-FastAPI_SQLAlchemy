from app.database import Base
from app.repositories.base import BaseRepository
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Ingredient(Base, BaseRepository):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    recipes = relationship(
        "Recipe", secondary="recipes_ingredients", back_populates="ingredients"
    )
