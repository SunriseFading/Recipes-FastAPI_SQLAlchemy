from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer)
    name = Column(String)
    description = Column(Text, nullable=True)
    time = Column(Integer)
    photo = Column(String, default="")

    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("Recipe", back_populates="steps")
