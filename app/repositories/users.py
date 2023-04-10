from app.models.users import User as UserModel
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=UserModel)

    async def create(self, instance, session: AsyncSession):
        instance.password = instance.hash_password()
        return await super().create(instance=instance, session=session)


user_repository = UserRepository()
