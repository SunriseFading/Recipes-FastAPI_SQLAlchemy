from app.services.ingredients import IngredientService
from app.services.steps import StepCRUD
from app.models.recipes import Recipe as RecipeModel
from app.models.recipes import RecipeIngredient as RecipeIngredientModel
from app.models.steps import Step as StepModel
from app.schemas.recipes import Ingredient as IngredientSchema
from app.schemas.recipes import Recipe as RecipeSchema
from app.schemas.recipes import RecipeParams as RecipeParamsSchema
from app.utils.messages import messages
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession


class RecipeService:
    @classmethod
    async def create(cls, recipe_schema: RecipeSchema, session: AsyncSession):
        recipe = await RecipeModel(
            name=recipe_schema.name, description=recipe_schema.description
        ).create(session=session)
        await IngredientService.bulk_create(
            recipe_id=recipe.id,
            ingredients_schema=recipe_schema.ingredients,
            session=session,
        )
        await StepCRUD.bulk_create(
            recipe_id=recipe.id, steps_schema=recipe_schema.steps, session=session
        )
        recipe.total_time = sum(step.time for step in recipe_schema.steps)
        return await recipe.update(session=session)

    @staticmethod
    async def get(id: int, session: AsyncSession):
        recipe = await RecipeModel.get(id=id, session=session)
        if recipe is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=messages.RECIPE_NOT_FOUND
            )
        return recipe

    @staticmethod
    async def get_all(params: RecipeParamsSchema, session: AsyncSession):
        return await RecipeModel.filter(
            session=session,
            order_by=params.order_by,
            average_rating=params.average_rating,
        )

    @staticmethod
    async def get_by_ingredients(
        ingredients: list[IngredientSchema], session: AsyncSession
    ):
        return await RecipeModel.filter_by_ingredients(
            ingredients=ingredients, session=session
        )

    @classmethod
    async def update(cls, id: int, recipe_schema: RecipeSchema, session: AsyncSession):
        recipe = await cls.get(id=id, session=session)
        recipe.name = recipe_schema.name
        recipe.description = recipe_schema.description
        recipes_ingredients = await RecipeIngredientModel.filter(
            recipe_id=recipe.id, session=session
        )
        await RecipeIngredientModel.bulk_delete(instances=recipes_ingredients, session=session)
        await StepModel.bulk_delete(instances=recipe.steps, session=session)
        await IngredientService.bulk_create(
            recipe_id=recipe.id,
            ingredients_schema=recipe_schema.ingredients,
            session=session,
        )
        await StepCRUD.bulk_create(
            recipe_id=recipe.id, steps_schema=recipe_schema.steps, session=session
        )
        recipe.total_time = sum(step.time for step in recipe_schema.steps)
        return await recipe.update(session=session)

    @classmethod
    async def delete(cls, id: int, session: AsyncSession):
        recipe = await cls.get(id=id, session=session)
        await recipe.delete(session=session)

    @classmethod
    async def upload_photo(cls, id: int, photo: UploadFile, session: AsyncSession):
        recipe = await cls.get(id=id, session=session)
        await recipe.upload_photo(photo=photo, session=session)

    @classmethod
    async def download_photo(cls, id: int, session: AsyncSession):
        recipe = await cls.get(id=id, session=session)
        return recipe.download_photo()

    @staticmethod
    async def update_rating(
        recipe: RecipeModel,
        review_rating: int,
        session: AsyncSession,
    ):
        recipe.reviews_count += 1
        if recipe.reviews_count == 1: recipe.average_rating = review_rating
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
        await recipe.update(session=session)
