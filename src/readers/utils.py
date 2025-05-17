from fastapi import HTTPException
from sqlalchemy import select, update, Result
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.models.ReaderModel import ReaderModel
from src.readers.schemas import ReaderBase, ReaderUpdate


async def get_readers(session: AsyncSession):
    stmt = select(ReaderModel).order_by(ReaderModel.id)
    result:Result = await session.execute(stmt)
    readers = await result.scalars().all()
    return readers

async def create_reader(session: AsyncSession, data: ReaderBase):
    try:
        reader = ReaderModel(**data.model_dump())
        session.add(reader)
        await session.commit()
        await session.refresh(reader)
        return reader
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="email must be unique")


async def get_reader(session: AsyncSession, reader_id: int):
    stmt = select(ReaderModel).where(ReaderModel.id == reader_id)
    reader = await session.execute(stmt)
    reader = reader.scalar_one_or_none()
    return reader

async def delete_reader(session: AsyncSession, book_id: int):
    reader = await get_reader(session, book_id)
    if reader:
        await session.delete(reader)
        await session.commit()
        return reader.name
    else:
        return False

async def update_reader(session: AsyncSession, reader_id: int, data: ReaderUpdate):
    reader = await get_reader(session, reader_id)
    if reader:
        stmt = (
            update(ReaderModel)
            .where(ReaderModel.id == reader_id)
            .values(**data.model_dump(exclude_unset=True))
            .returning(ReaderModel)
        )
        result = await session.execute(stmt)
        updated_reader = result.scalar_one()
        await session.commit()
        await session.refresh(updated_reader)
        return updated_reader
    return None