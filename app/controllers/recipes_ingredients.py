from app.models.ingredients import Ingredient as IngredientModel
from app.models.recipes_ingredients import RecipeIngredient as RecipeIngredientModel
from app.repositories.recipe_ingredients import recipe_ingredient_repository
from sqlalchemy.ext.asyncio import AsyncSession


class RecipeIngredientController:
    def __init__(self, recipe_ingredient_repository):
        self.recipe_ingredient_repository = recipe_ingredient_repository

    async def bulk_create(
        self, recipe_id: int, ingredients: list[IngredientModel], session: AsyncSession
    ):
        recipes_ingredients = []
        for ingredient in ingredients:
            recipe_ingredient = RecipeIngredientModel(
                recipe_id=recipe_id, ingredient_id=ingredient.id
            )
            recipes_ingredients.append(recipe_ingredient)
        return await self.recipe_ingredient_repository.bulk_create(
            instances=recipes_ingredients, session=session
        )

    async def filter(self, session: AsyncSession, **kwargs):
        return await self.recipe_ingredient_repository.filter(**kwargs, session=session)

    async def bulk_delete(
        self, recipes_ingredients: list[RecipeIngredientModel], session: AsyncSession
    ):
        await self.recipe_ingredient_repository.bulk_delete(
            instances=recipes_ingredients, session=session
        )


recipe_ingredient_controller = RecipeIngredientController(
    recipe_ingredient_repository=recipe_ingredient_repository
)
