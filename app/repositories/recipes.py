from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository


class RecipeRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session