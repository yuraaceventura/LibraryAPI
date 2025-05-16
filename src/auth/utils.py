from passlib.context import CryptContext
import datetime
import jwt
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import settings
from database.models import UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = (
            datetime.datetime.now(datetime.UTC) + settings.jwt.token_expiration_delta
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt.PUBLIC_KEY,
        algorithm=settings.jwt.ALGORITHM,
    )
    return encoded_jwt

async def get_user_by_id(session: AsyncSession,
                         user_id:str
                         ):

    stmt = Select(UserModel).where(UserModel.id == user_id)
    user = session.scalar(stmt)
    return user
