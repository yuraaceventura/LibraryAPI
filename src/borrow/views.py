from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_helper import db_helper
from database.models import BorrowedBooksTable
from src.books.utils import get_book
from src.borrow.schemas import BorrowSchema, Borrow
from src.borrow import utils
from src.readers.utils import get_reader

router = APIRouter(tags=["Borrow"], prefix="/borrow")

@router.post("")
async def borrow_book(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                 data: BorrowSchema):
    book = await get_book(session, data.book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available == 0:
        raise HTTPException(status_code=400, detail="Book not available")

    reader = await get_reader(session, data.reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")

    is_borrowed = await utils.check_borrow(session, data)
    if is_borrowed:
        raise HTTPException(status_code=400, detail="Book is already borrowed by this reader")

    borrow = await utils.create_borrow(session, data)
    return BorrowSchema.model_validate(borrow.__dict__)

@router.post("/{borrow_id}")
async def return_book(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                      borrow_id: int):
    borrow:BorrowedBooksTable = await utils.get_borrow(session, borrow_id)
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")

    if borrow.returned_at is not None:
        raise HTTPException(status_code=400, detail="Book already returned")

    borrow = await utils.return_book(session, borrow)
    return Borrow.model_validate(borrow.__dict__)


@router.get("")
async def get_borrows(session: Annotated[AsyncSession, Depends(db_helper.get_session)]):
    return await utils.get_borrows(session)