import bcrypt
from app.database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)

    def hash_password(self) -> str:
        return bcrypt.hashpw(self.password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, unhashed_password: str) -> bool:
        return bcrypt.checkpw(unhashed_password.encode(), self.password.encode())
