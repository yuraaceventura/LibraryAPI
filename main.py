from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database.base import Base
from database.db_helper import db_helper
from src.auth.views import router as auth_router
from src.books.views import router as books_router
from src.readers.views import router as readers_router
from src.borrow.views import router as borrow_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(books_router)
app.include_router(readers_router)
app.include_router(borrow_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=1)