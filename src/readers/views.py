from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_409_CONFLICT

from database.db_helper import db_helper
from src.auth.dependencies import get_current_user
from src.readers import utils
from src.readers.schemas import ReaderUpdate, ReaderBase, ReaderFull

router = APIRouter(prefix="/readers", tags=["Readers"])


@router.get("", dependencies=[Depends(get_current_user)])
async def get_readers(session: Annotated[AsyncSession, Depends(db_helper.get_session)]):
    return await utils.get_readers(session)

@router.post("", dependencies=[Depends(get_current_user)])
async def create_reader(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                      reader: ReaderBase,
                      ) -> ReaderFull:
    reader = await utils.create_reader(session, reader)
    if reader:
        return reader
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Reader already exists")


@router.get("/{reader_id}", dependencies=[Depends(get_current_user)])
async def get_reader_by_id(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                         reader_id: int,) -> ReaderFull:
    reader = await utils.get_reader(session, reader_id)
    if reader:
        return reader
    else:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Reader does not exist")


@router.delete("/{reader_id}", dependencies=[Depends(get_current_user)])
async def delete_reader(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                        reader_id: int,) -> ReaderFull:
    reader = await utils.delete_reader(session, reader_id)
    if reader:
        return reader
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Couldn't find this reader")


@router.patch("/{reader_id}", dependencies=[Depends(get_current_user)])
async def update_reader(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                      reader_id: int,
                      reader: ReaderUpdate) -> ReaderFull:
    if len(reader.model_dump()) > 0:
        reader_updated = await utils.update_reader(session, reader_id, reader)
        return reader_updated

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Something went wrong")
