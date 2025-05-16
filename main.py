import uvicorn
from fastapi import FastAPI
from src.auth.views import router as auth_router
from src.books.views import router as books_router
app = FastAPI()

app.include_router(auth_router)
app.include_router(books_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=1)