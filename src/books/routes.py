from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.books.schemas import BookUpdateModel, BookCreateModel
from src.db.main import get_session
from src.books.models import Book
from typing import List
from src.auth.dependencies import AccessTokenBearer

book_router = APIRouter()
book_service = BookService()

access_token_bearer = AccessTokenBearer()

@book_router.get("/",response_model=List[Book])
async def get_all_books(session:AsyncSession = Depends(get_session),user=Depends(access_token_bearer)):
    books = await book_service.get_all_books(session)
    return books

@book_router.get("/{book_uid}",response_model=Book)
async def get_book_by_id(book_uid: str,session:AsyncSession = Depends(get_session),user=Depends(access_token_bearer))->Book:
    book = await book_service.get_book(book_uid , session)

    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@book_router.post("/", status_code=status.HTTP_201_CREATED,response_model=Book)
async def create_book(book: BookCreateModel,session:AsyncSession = Depends(get_session),user=Depends(access_token_bearer))->Book:
    new_book = await book_service.create_book(book,session)
    return new_book

@book_router.patch("/{book_uid}")
async def update_book(book_uid: str, book_update_data:BookUpdateModel,session:AsyncSession = Depends(get_session),user=Depends(access_token_bearer))->Book:
    updated_book = await book_service.update_book(book_uid ,book_update_data, session)

    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=404, detail="Book not found")
    

@book_router.delete("/{book_uid}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str,session:AsyncSession = Depends(get_session),user=Depends(access_token_bearer)):
    deleted_book = await book_service.delete_book(book_uid,session)

    if deleted_book:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")