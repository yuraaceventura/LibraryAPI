from pydantic import EmailStr
from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import Base

class ReaderModel(Base):
    __tablename__ = 'readers'

    id : Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[EmailStr] = mapped_column(String, index=True, unique=True)
    borrowed = relationship("BorrowedBooksTable", back_populates="reader")