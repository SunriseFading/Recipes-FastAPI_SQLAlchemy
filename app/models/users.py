import bcrypt
from app.database import Base
from app.repositories.base import BaseRepository
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, BaseRepository):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)

    def hash_password(self) -> str:
        return bcrypt.hashpw(self.password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, unhashed_password: str) -> bool:
        return bcrypt.checkpw(unhashed_password.encode(), self.password.encode())

    async def create(self, session: AsyncSession):
        self.password = self.hash_password()
        return await super().create(session=session)

    async def update(self, session: AsyncSession):
        self.password = self.hash_password()
        return await super().create(session=session)
