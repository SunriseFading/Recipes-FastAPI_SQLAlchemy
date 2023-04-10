from app.models.ingredients import Ingredient as IngredientModel
from app.repositories.base import BaseRepository


class IngredientRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=IngredientModel)


ingredient_repository = IngredientRepository()
