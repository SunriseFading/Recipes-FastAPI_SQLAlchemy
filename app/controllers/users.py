from app.models.users import User as UserModel
from app.repositories.users import user_repository
from app.schemas.users import User as UserSchema
from sqlalchemy.ext.asyncio import AsyncSession


class UserController:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def create(self, user_schema: UserSchema, session: AsyncSession):
        user = UserModel(email=user_schema.email, password=user_schema.password)
        user = await self.user_repository.create(instance=user, session=session)
        return user

    async def get(self, email: str, session: AsyncSession):
        return await self.user_repository.get(email=email, session=session)


user_controller = UserController(user_repository=user_repository)
