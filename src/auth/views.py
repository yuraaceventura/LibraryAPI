from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Form, Response
from fastapi.security import OAuth2PasswordRequestFormStrict
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import authenticate_user, get_user, register_user, get_current_user
from .schemas import UserCreate, Token
from database.models.UserModel import UserModel
from .utils import (
    get_password_hash,
    create_access_token,
)
from database.db_helper import db_helper

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
async def login(
    response: Response,
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    user: UserCreate,
):
    user_db: UserModel = await authenticate_user(session, user.email, user.password)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(data={"sub": str(user_db.id)})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=3600
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register(
    session: AsyncSession = Depends(db_helper.get_session),
    user: UserCreate = Form()
):
    user_db: UserModel = await get_user(session, user.email)
    if user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already registered",
        )
    hashed_password = get_password_hash(user.password)
    new_user = await register_user(session, user.email,hashed_password)
    return new_user

