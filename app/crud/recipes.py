from app.crud.ingredients import IngredientCRUD
from app.crud.steps import StepCRUD
from app.models.recipes import Recipe as m_Recipe
from app.models.recipes import RecipeIngredient as m_RecipeIngredient
from app.models.steps import Step as m_Step
from app.schemas.recipes import Ingredient as s_Ingredient
from app.schemas.recipes import Recipe as s_Recipe
from app.schemas.recipes import RecipeParams
from app.utils.messages import messages
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession


class RecipeCRUD:
    @classmethod
    async def create(cls, recipe_schema: s_Recipe, session: AsyncSession):
        recipe = await m_Recipe(
            name=recipe_schema.name, description=recipe_schema.description
        ).create(session=session)
        await IngredientCRUD.bulk_create(
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
        recipe = await m_Recipe.get(id=id, session=session)
        if recipe is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=messages.RECIPE_NOT_FOUND
            )
        return recipe

    @staticmethod
    async def get_all(recipe_params: RecipeParams, session: AsyncSession):
        return await m_Recipe.filter(
            session=session,
            order_by=recipe_params.order_by,
            average_rating=recipe_params.average_rating,
        )

    @staticmethod
    async def get_by_ingredients(
        ingredients: list[s_Ingredient], session: AsyncSession
    ):
        return await m_Recipe.filter_by_ingredients(
            ingredients=ingredients, session=session
        )

    @classmethod
    async def update(cls, id: int, recipe_schema: s_Recipe, session: AsyncSession):
        recipe = await cls.get(id=id, session=session)
        recipe.name = recipe_schema.name
        recipe.description = recipe_schema.description
        recipes_ingredients = await m_RecipeIngredient.filter(
            recipe_id=recipe.id, session=session
        )
        await m_RecipeIngredient.delete(instances=recipes_ingredients, session=session)
        await m_Step.delete(instances=recipe.steps, session=session)
        await IngredientCRUD.bulk_create(
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
        await m_Recipe.delete(instances=recipe, session=session)

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
        recipe: m_Recipe,
        review_rating: int,
        session: AsyncSession,
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
        await recipe.update(session=session)
