from pydantic import BaseModel, EmailStr


class ReaderBase(BaseModel):
    name:str
    email:EmailStr

class ReaderUpdate(ReaderBase):
    name:str | None
    email:EmailStr | None

class ReaderFull(ReaderBase):
    id: int