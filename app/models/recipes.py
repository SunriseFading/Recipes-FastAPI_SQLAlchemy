from app.database import Base
from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.orm import relationship


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text, nullable=True)
    photo = Column(String, default="")

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


fields = [column.name for column in Recipe.__table__.columns]
