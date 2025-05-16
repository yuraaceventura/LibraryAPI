import uuid

from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from database.base import Base


class UserModel(Base):
    __tablename__ = 'users'

    id : Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[EmailStr] = mapped_column(String, index=True, unique=True)
    hashed_password: Mapped[str]