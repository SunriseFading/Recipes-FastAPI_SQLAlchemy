from app.database import Base
from app.repositories.base import BaseRepository
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Review(Base, BaseRepository):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))

    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("Recipe", back_populates="reviews")
