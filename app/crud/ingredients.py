from app.models.ingredients import Ingredient as m_Ingredient
from app.models.recipes import RecipeIngredient as m_RecipeIngredient
from app.schemas.ingredients import Ingredient as s_Ingredient
from sqlalchemy.ext.asyncio import AsyncSession


class IngredientCRUD:
    @staticmethod
    async def bulk_create(
        recipe_id: int, ingredients_schema: list[s_Ingredient], session: AsyncSession
    ):
        for ingredient_schema in ingredients_schema:
            ingredient = await m_Ingredient(name=ingredient_schema.name).get_or_create(
                session=session
            )
            await m_RecipeIngredient(
                recipe_id=recipe_id, ingredient_id=ingredient.id
            ).create(session=session)
