from app.services.recipes import RecipeService
from app.database import async_session
from app.models.recipes import Recipe as RecipeModel
from app.schemas.ingredients import Ingredient
from app.schemas.recipes import Recipe as RecipeSchema
from app.schemas.steps import Step


async def create_init_data(
    recipe_schema: RecipeSchema = RecipeSchema(
        name="test recipe",
        description="test desc",
        ingredients=[Ingredient(name="onion"), Ingredient(name="tomato")],
        steps=[
            Step(
                name="prepare",
                time=0,
                description="",
            ),
            Step(
                name="middle",
                time=0,
                description="",
            ),
        ],
    )
):
    async with async_session() as session:
        if not (await RecipeModel.all(session=session)):
            for i in range(1, 101):
                recipe_schema.name = f"№{i} Spaghetti Bolognese"
                recipe_schema.description = (
                    f"№{i} A classic Italian dish that's perfect for a hearty meal."
                )
                await RecipeService.create(recipe_schema=recipe_schema, session=session)
