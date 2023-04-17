from app.models.ingredients import Ingredient as IngredientModel
from app.repositories.ingredients import ingredient_repository
from app.schemas.ingredients import Ingredient as IngredientSchema
from sqlalchemy.ext.asyncio import AsyncSession


class IngredientController:
    def __init__(self, ingredient_repository):
        self.ingredient_repository = ingredient_repository

    async def bulk_create(
        self, ingredients_schema: list[IngredientSchema], session: AsyncSession
    ):
        ingredients = []
        for ingredient_schema in ingredients_schema:
            ingredient = await self.ingredient_repository.get_or_create(
                instance=IngredientModel(name=ingredient_schema.name), session=session
            )
            ingredients.append(ingredient)
        return ingredients


ingredient_controller = IngredientController(ingredient_repository=ingredient_repository)
