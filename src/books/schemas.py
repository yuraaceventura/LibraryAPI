from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    author: str
    published_at: int | None
    ISBN: str | None
    available: int

    model_config = ConfigDict(from_attributes=True)


class BookRead(BookBase):
    id: int


class BookUpdate(BookBase):
    title: str | None = None
    author: str | None = None
    published_at: int | None = None
    ISBN: str | None = None
    available: int | None = None