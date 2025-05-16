from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class BorrowedBooksTable(Base):
    __tablename__ = 'borrowed_books'

    id : Mapped[int] = mapped_column(primary_key=True)
    reader_id: Mapped[int] = ForeignKey("readers.id")
    book_id: Mapped[int] = ForeignKey("books.id")
    borrowed_at : Mapped[datetime] = mapped_column(default=datetime.now())
    returned_at : Mapped[datetime] = mapped_column(default=None, onupdate=datetime.now())

    book = relationship("books", back_populates="borrow_records")
    reader = relationship("readers", back_populates="borrow_records")