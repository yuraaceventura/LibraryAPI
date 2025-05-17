import datetime

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import BorrowedBooksTable, BookModel
from src.borrow.schemas import BorrowSchema


async def check_borrow(session: AsyncSession,
                       data: BorrowSchema):

    stmt = select(BorrowedBooksTable).where(
            and_(
                BorrowedBooksTable.reader_id == data.reader_id,
                BorrowedBooksTable.book_id == data.book_id,
                BorrowedBooksTable.returned_at == None
            )
        )
    result = await session.execute(stmt)
    borrowed = result.scalar_one_or_none()
    if borrowed:
        return True
    else:
        return False



async def create_borrow(session: AsyncSession, data: BorrowSchema):
    new_borrow = BorrowedBooksTable(reader_id=data.reader_id, book_id=data.book_id)
    session.add(new_borrow)

    stmt = update(BookModel).where(BookModel.id == data.book_id).values(available=BookModel.available - 1)
    await session.execute(stmt)
    await session.commit()
    await session.refresh(new_borrow)
    return new_borrow

async def get_borrow(session: AsyncSession, borrow_id: int):
    stmt = select(BorrowedBooksTable).where(BorrowedBooksTable.id == borrow_id)
    result = await session.execute(stmt)
    borrowed = result.scalar_one_or_none()
    return borrowed


async def return_book(session: AsyncSession, borrow: BorrowedBooksTable):
    stmt = update(BorrowedBooksTable).where(BorrowedBooksTable.id == borrow.id).values().returning(BorrowedBooksTable.book_id)
    book_id = await session.execute(stmt)
    stmt = update(BookModel).where(BookModel.id == book_id).values(available=BookModel.available + 1)
    await session.execute(stmt)
    await session.commit()
    await session.refresh(borrow)
    return borrow


async def get_borrows(session:AsyncSession):
    stmt = select(BorrowedBooksTable).where(BorrowedBooksTable.returned_at == None)
    result = await session.execute(stmt)
    borrowed_books = result.scalars().all()
    return borrowed_books

