from datetime import datetime

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import Base


class BookModel(Base):
    __tablename__ = 'books'
    __table_args__ = (
        CheckConstraint("available >= 0", name="check_in_stock_constraint"),
    )

    id : Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    published_at: Mapped[datetime | None]
    ISBN: Mapped[str | None] = mapped_column(unique=True)
    available: Mapped[int] = mapped_column(default=1)
    borrowed = relationship("BorrowedBooksTable", back_populates="book")