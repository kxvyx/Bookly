from fastapi import FastAPI
from src.books.routes import books_router


version = "v1"
app = FastAPI(
    title="Books API",
    description="A FastAPI for managing books",
    version=version,
)

app.include_router(books_router, prefix=f"/api/{version}/books", tags=["books"])




