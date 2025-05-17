from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.db_helper import db_helper
from src.auth.dependencies import get_current_user
from src.books.schemas import BookBase, BookUpdate, BookRead
from src.books import utils
router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", dependencies=[Depends(get_current_user)])
async def get_books(session: Annotated[AsyncSession, Depends(db_helper.get_session)]) -> list[BookRead]:
    return await utils.get_books(session)

@router.post("", dependencies=[Depends(get_current_user)])
async def create_book(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                      book: BookBase,
                      ) -> BookRead:
    if book := await utils.create_book(session, book):
        return book
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="ISBN must be unique")

@router.get("/{book_id}", dependencies=[Depends(get_current_user)])
async def get_book_by_id(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                         book_id: int,) -> BookRead:
    if book := await utils.get_book(session, book_id):
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Book not found")

@router.delete("/{book_id}", dependencies=[Depends(get_current_user)])
async def delete_book(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                      book_id: int,) -> BookRead:
    book = await utils.delete_book(session, book_id)
    if book:
        return BookRead.model_validate(book)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Book not found")


@router.patch("/{book_id}", dependencies=[Depends(get_current_user)])
async def update_book(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                      book_id: int,
                      book: BookUpdate) -> BookRead:
    if len(book.model_dump(exclude_none=True)) > 0:
        book_updated = await utils.update_book(session, book_id, book)
        if book_updated:
            return BookRead.model_validate(book_updated.__dict__)
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail="Something went wrong")
