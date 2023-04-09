from app.models.ingredients import Ingredient as IngredientModel
from app.models.recipes import RecipeIngredient as RecipeIngredientModel
from app.schemas.ingredients import Ingredient as IngredientSchema
from sqlalchemy.ext.asyncio import AsyncSession


class IngredientService:
    @staticmethod
    async def bulk_create(
        recipe_id: int, ingredients_schema: list[IngredientSchema], session: AsyncSession
    ):
        for ingredient_schema in ingredients_schema:
            ingredient = await IngredientModel(name=ingredient_schema.name).get_or_create(
                session=session
            )
            await RecipeIngredientModel(
                recipe_id=recipe_id, ingredient_id=ingredient.id
            ).create(session=session)
