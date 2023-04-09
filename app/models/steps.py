from app.database import Base
from app.repositories.base import BaseRepository
from app.repositories.photo import PhotoRepository
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class Step(Base, BaseRepository, PhotoRepository):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer)
    name = Column(String)
    description = Column(Text, nullable=True)
    time = Column(Integer)
    photo = Column(String, nullable=True)

    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("Recipe", back_populates="steps")
