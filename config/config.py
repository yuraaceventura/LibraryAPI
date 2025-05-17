import pathlib
from datetime import timedelta

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict, BaseSettings

BASE_DIR = pathlib.Path(__file__).parent.absolute()

ENV_FILE_PATH = BASE_DIR / '.env.example'


class SettingsBase(BaseSettings):

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra="ignore")


class DatabaseSettings(SettingsBase):
    NAME:str
    USER:str
    PASS:str
    HOST:str
    PORT:str

    def get_url(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"

    model_config = SettingsConfigDict(env_prefix="DB_")

class JWTSettings(SettingsBase):
    token_expiration_delta:timedelta = timedelta(minutes=20)
    PUBLIC_KEY: str
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_prefix="JWT_")

class Settings(BaseModel):
    jwt : JWTSettings = Field(default_factory=JWTSettings)
    database : DatabaseSettings = Field(default_factory=DatabaseSettings)

settings = Settings()
