from fastapi import APIRouter, HTTPException, status
from src.books.books_data import books
from src.books.schemas import BookUpdateModel

books_router = APIRouter()


@books_router.get("/")
async def get_all_books():
    return books

@books_router.get("/{book_id}")
async def get_book_by_id(book_id: int)->dict:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@books_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: dict)->dict:
    book["id"] = len(books) + 1
    books.append(book)
    return book

@books_router.patch("/{book_id}")
async def update_book(book_id: int, book_update_data:BookUpdateModel)->dict:
    for book in books:
        if book["id"] == book_id:
            update_data = book_update_data.model_dump(exclude_unset=True)
            book.update(update_data)
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@books_router.delete("/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")