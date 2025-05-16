from pydantic import EmailStr
from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import Base
from database.models.BookModel import BookModel


class ReaderModel(Base):
    __tablename__ = 'readers'
    __table_args__ = (
        CheckConstraint("in_stock >= 0", name="check_in_stock_constraint"),
    )
    id : Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[EmailStr] = mapped_column(String, index=True, unique=True)
    borrowed = relationship("borrowed_books", back_populates="reader_id")