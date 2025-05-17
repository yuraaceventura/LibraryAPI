from fastapi import HTTPException
from sqlalchemy import select, update, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.models.BookModel import BookModel
from src.books.schemas import BookBase, BookUpdate


async def get_books(session: AsyncSession):
    stmt = select(BookModel).order_by(BookModel.id)
    result:Result = await session.execute(stmt)
    books = result.scalars().all()
    return books

async def create_book(session: AsyncSession, data: BookBase):
    try:
        book = BookModel(**data.model_dump())
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book
    except Exception as e:
        return False


async def get_book(session: AsyncSession, book_id: int):
    stmt = select(BookModel).where(BookModel.id == book_id)
    book = await session.execute(stmt)
    book = book.scalar_one_or_none()
    return book

async def delete_book(session: AsyncSession, book_id: int):
    book = await get_book(session, book_id)
    if book:
        stmt = delete(BookModel).where(BookModel.id == book_id).returning(BookModel)
        result = await session.execute(stmt)
        book = result.scalar_one()
        await session.commit()
        return book
    else:
        return False

async def update_book(session: AsyncSession, book_id: int, data: BookUpdate):
    book = await get_book(session, book_id)
    if book:
        stmt = (
            update(BookModel)
            .where(BookModel.id == book_id)
            .values(**data.model_dump(exclude_unset=True))
            .returning(BookModel)
        )
        result = await session.execute(stmt)
        updated_book = result.scalar_one()
        await session.commit()
        await session.refresh(updated_book)
        return updated_book
    return None