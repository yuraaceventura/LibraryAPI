import pathlib

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict, BaseSettings

BASE_DIR = pathlib.Path(__file__).parent.absolute()

ENV_FILE_PATH = BASE_DIR / '.env.example'


class SettingsBase(BaseSettings):

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH)


class DatabaseSettings(SettingsBase):
    NAME:str
    USER:str
    PASS:str
    HOST:str
    PORT:str

    def get_url(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"

    model_config = SettingsConfigDict(env_prefix="DB_")


class Settings(BaseModel):
    database : DatabaseSettings = Field(default_factory=DatabaseSettings)

settings = Settings()
