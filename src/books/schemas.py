from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    published_at: int | None
    ISBN: str | None
    available: int

class BookRead(BookBase):
    id: int


class BookUpdate(BookBase):
    title: str | None
    author: str | None
    published_at: int | None
    ISBN: str | None
    available: int | None