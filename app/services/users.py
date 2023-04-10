from app.models.users import User as UserModel
from app.repositories.users import user_repository
from app.schemas.users import User as UserSchema
from app.utils.messages import messages
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def create(self, user_schema: UserSchema, session: AsyncSession):
        user = UserModel(email=user_schema.email, password=user_schema.password)
        user = await self.user_repository.create(instance=user, session=session)
        return user

    async def get(self, email: str, session: AsyncSession):
        user = await self.user_repository.get(email=email, session=session)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
            )
        return user


user_service = UserService(user_repository=user_repository)
