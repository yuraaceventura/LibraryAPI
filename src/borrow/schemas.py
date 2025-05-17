from datetime import datetime

from pydantic import BaseModel


class BorrowSchema(BaseModel):
    reader_id:int
    book_id:int

class Borrow(BaseModel):
    id: int
    reader_id:int
    book_id:int
    returned_at: datetime
    borrowed_at: datetime

