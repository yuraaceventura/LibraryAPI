import jwt
from fastapi import Depends, HTTPException, status
from fastapi.params import Header
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import EmailStr
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from src.auth.schemas import TokenData
from src.auth.utils import verify_password, get_password_hash
from database.models import UserModel
from config.config import settings
from database.db_helper import db_helper

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_user(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    email: EmailStr,
):
    stmt = select(UserModel).where(UserModel.email == email)
    result: UserModel = await session.execute(stmt)
    return result


async def authenticate_user(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
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
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    token = Annotated[str, Header(alias="Authorization")],
):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.jwt.public_key, algorithms=[settings.jwt.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exceptions
        token_data = TokenData(
            username=username, access_token=token, token_type="Bearer"
        )
    except PyJWTError:
        raise credentials_exceptions
    user = await get_user(
        session,
        token_data.username,
    )
    if user is None:
        raise credentials_exceptions
    return user
