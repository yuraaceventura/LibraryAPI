from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.db_helper import db_helper
from src.auth.dependencies import get_current_user
from src.readers import utils
from src.readers.schemas import ReaderUpdate, ReaderBase

router = APIRouter(prefix="/readers", tags=["Readers"])


@router.get("/", dependencies=[Depends(get_current_user)])
async def get_readers(session: Annotated[AsyncSession, Depends(db_helper.get_session)]):
    return await utils.get_readers(session)

@router.post("/", dependencies=[Depends(get_current_user)])
async def create_reader(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                      reader: ReaderBase,
                      ) -> ReaderBase:
    return await utils.create_reader(session, reader)

@router.get("/{reader_id}", dependencies=[Depends(get_current_user)])
async def get_reader_by_id(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                         reader_id: int,):
    return await utils.get_reader(session, reader_id)

@router.delete("/{reader_id}", dependencies=[Depends(get_current_user)])
async def delete_reader(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                        reader_id: int,):
    reader = await utils.delete_reader(session, reader_id)
    if reader:
        return {"msg": "reader deleted successfully",
                "reader" : reader}
    else:
        return {"msg": "Couldn't find this reader",}


@router.patch("/{reader_id}", dependencies=[Depends(get_current_user)])
async def update_reader(session: Annotated[AsyncSession, Depends(db_helper.get_session)],
                      reader_id: int,
                      reader: ReaderUpdate) -> ReaderBase:
    if len(reader.model_dump()) > 0:
        reader_updated = await utils.update_reader(session, reader_id, reader)
        return ReaderBase.model_validate(reader_updated.__dict__)

    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail="Something went wrong")
