from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


from database.models.BookModel import BookModel
from database.models.ReaderModel import ReaderModel

class BorrowedBooksTable(Base):
    __tablename__ = 'borrowed_books'

    id : Mapped[int] = mapped_column(primary_key=True)
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    borrowed_at : Mapped[datetime] = mapped_column(default=datetime.now())
    returned_at : Mapped[datetime] = mapped_column(default=None, onupdate=datetime.now())

    book = relationship(BookModel, back_populates="borrowed")
    reader = relationship(ReaderModel, back_populates="borrowed")