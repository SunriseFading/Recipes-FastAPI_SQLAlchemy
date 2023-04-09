from app.database import Base
from app.repositories.base import BaseRepository
from app.repositories.photo import PhotoRepository
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship


class RecipeIngredient(Base, BaseRepository):
    __tablename__ = "recipes_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True, index=True)
    ingredient_id = Column(
        Integer, ForeignKey("ingredients.id"), primary_key=True, index=True
    )


class Recipe(Base, BaseRepository, PhotoRepository):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text, nullable=True)
    photo = Column(String, nullable=True)

    total_time = Column(Integer, default=0)
    average_rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, default=0)

    ingredients = relationship(
        "Ingredient",
        secondary="recipes_ingredients",
        back_populates="recipes",
        lazy="selectin",
    )
    steps = relationship(
        "Step", back_populates="recipe", cascade="all,delete", lazy="selectin"
    )
    reviews = relationship("Review", back_populates="recipe", cascade="all,delete")

    @classmethod
    async def filter_by_ingredients(cls, ingredients: list, session: AsyncSession):
        query = select(cls).filter(
            and_(
                *(
                    cls.ingredients.any(name=ingredient.name)
                    for ingredient in ingredients
                )
            )
        )
        if result := await session.execute(query):
            return result.scalars().all()


fields = [column.name for column in Recipe.__table__.columns]
