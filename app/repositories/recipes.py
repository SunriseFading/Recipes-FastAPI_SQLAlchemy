from app.models.recipes import Recipe as RecipeModel
from app.repositories.base import BaseRepository
from app.repositories.photo import PhotoRepository
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class RecipeRepository(BaseRepository, PhotoRepository):
    def __init__(self):
        super().__init__(model=RecipeModel)

    async def filter_by_ingredients(self, ingredients: list, session: AsyncSession):
        query = select(self.model).filter(
            and_(
                *(
                    self.model.ingredients.any(name=ingredient.name)
                    for ingredient in ingredients
                )
            )
        )
        if result := await session.execute(query):
            return result.scalars().all()


recipe_repository = RecipeRepository()
