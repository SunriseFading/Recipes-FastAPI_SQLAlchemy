from app.models.recipes_ingredients import RecipeIngredient as RecipeIngredient
from app.repositories.base import BaseRepository


class RecipeIngredientRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=RecipeIngredient)


recipe_ingredient_repository = RecipeIngredientRepository()
