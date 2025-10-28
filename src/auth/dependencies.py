from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status, Request
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import settings
from database.db_helper import db_helper
from database.models.UserModel import UserModel
from src.auth.schemas import TokenData
from src.auth.utils import verify_password, get_user_by_id


async def get_user(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    email: EmailStr,
):
    stmt = select(UserModel).where(UserModel.email == email)
    result: UserModel = await session.scalar(stmt)
    return result


async def authenticate_user(
    session: AsyncSession,
    email: EmailStr,
    password: str,
):
    user: UserModel = await get_user(session, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def register_user(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    email: EmailStr,
    password: str
):
    user = UserModel(email = email, hashed_password = password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user.id



async def get_current_user(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
):
    token = request.cookies.get("access_token")
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.jwt.PUBLIC_KEY, algorithms=[settings.jwt.ALGORITHM]
        )
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exceptions
        token_data = TokenData(
            sub=sub, access_token=token, token_type="Bearer"
        )
    except Exception as e:
        raise credentials_exceptions
    user = await get_user_by_id(
        session,
        token_data.sub,
    )
    if user is None:
        raise credentials_exceptions
    return user
