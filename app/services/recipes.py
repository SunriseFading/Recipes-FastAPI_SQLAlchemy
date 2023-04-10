from app.models.recipes import Recipe as RecipeModel
from app.repositories.recipes import recipe_repository
from app.schemas.recipes import Ingredient as IngredientSchema
from app.schemas.recipes import Recipe as RecipeSchema
from app.schemas.recipes import RecipeParams as RecipeParamsSchema
from app.services.ingredients import ingredient_service
from app.services.recipes_ingredients import recipe_ingredient_service
from app.services.steps import step_service
from app.utils.messages import messages
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession


class RecipeService:
    def __init__(
        self,
        recipe_repository,
        ingredient_service,
        recipe_ingredient_service,
        step_service,
    ):
        self.recipe_repository = recipe_repository
        self.ingredient_service = ingredient_service
        self.recipe_ingredient_service = recipe_ingredient_service
        self.step_service = step_service

    async def create(self, recipe_schema: RecipeSchema, session: AsyncSession):
        recipe = await self.recipe_repository.create(
            instance=RecipeModel(
                name=recipe_schema.name, description=recipe_schema.description
            ),
            session=session,
        )

        ingredients = await self.ingredient_service.bulk_create(
            ingredients_schema=recipe_schema.ingredients, session=session
        )

        await self.recipe_ingredient_service.bulk_create(
            recipe_id=recipe.id, ingredients=ingredients, session=session
        )

        await self.step_service.bulk_create(
            recipe_id=recipe.id, steps_schema=recipe_schema.steps, session=session
        )

        recipe.total_time = sum(step.time for step in recipe_schema.steps)
        return await self.recipe_repository.update(instance=recipe, session=session)

    async def get(self, id: int, session: AsyncSession):
        recipe = await self.recipe_repository.get(id=id, session=session)
        if recipe is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=messages.RECIPE_NOT_FOUND
            )
        return recipe

    async def get_all(self, params: RecipeParamsSchema, session: AsyncSession):
        return await self.recipe_repository.filter(
            order_by=params.order_by,
            average_rating=params.average_rating,
            session=session,
        )

    async def get_by_ingredients(
        self, ingredients: list[IngredientSchema], session: AsyncSession
    ):
        return await self.recipe_repository.filter_by_ingredients(
            ingredients=ingredients, session=session
        )

    async def update(self, id: int, recipe_schema: RecipeSchema, session: AsyncSession):
        recipe = await self.get(id=id, session=session)
        recipe.name = recipe_schema.name
        recipe.description = recipe_schema.description

        recipes_ingredients = await self.recipe_ingredient_service.filter(
            recipe_id=recipe.id, session=session
        )
        await self.recipe_ingredient_service.bulk_delete(
            recipes_ingredients=recipes_ingredients, session=session
        )

        await self.step_service.bulk_delete(steps=recipe.steps, session=session)

        ingredients = await self.ingredient_service.bulk_create(
            ingredients_schema=recipe_schema.ingredients, session=session
        )

        await self.recipe_ingredient_service.bulk_create(
            recipe_id=recipe.id, ingredients=ingredients, session=session
        )

        await self.step_service.bulk_create(
            recipe_id=recipe.id, steps_schema=recipe_schema.steps, session=session
        )

        recipe.total_time = sum(step.time for step in recipe_schema.steps)
        return await self.recipe_repository.update(instance=recipe, session=session)

    async def delete(self, id: int, session: AsyncSession):
        recipe = await self.get(id=id, session=session)
        await self.recipe_repository.delete(instance=recipe)

    async def upload_photo(self, id: int, photo: UploadFile, session: AsyncSession):
        recipe = await self.get(id=id, session=session)
        await self.recipe_repository.upload_photo(
            instance=recipe, photo=photo, session=session
        )

    async def download_photo(self, id: int, session: AsyncSession):
        recipe = await self.get(id=id, session=session)
        return self.recipe_repository.download_photo(instance=recipe)

    async def update_rating(
        self, recipe: RecipeModel, review_rating: int, session: AsyncSession
    ):
        recipe.reviews_count += 1
        if recipe.reviews_count == 1:
            recipe.average_rating = review_rating
        else:
            recipe.average_rating = round(
                (
                    (
                        (recipe.average_rating * (recipe.reviews_count - 1))
                        + review_rating
                    )
                    / recipe.reviews_count
                ),
                1,
            )
        await self.recipe_repository.update(instance=recipe, session=session)


recipe_service = RecipeService(
    recipe_repository=recipe_repository,
    ingredient_service=ingredient_service,
    recipe_ingredient_service=recipe_ingredient_service,
    step_service=step_service,
)
