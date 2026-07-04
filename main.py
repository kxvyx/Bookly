from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Hello FastAPI"}

# @app.get("/greet")
# async def greet(name: Optional[str]="user"):
#     return {"message": f"Hello, {name}!"}

# class BookCreateModel(BaseModel):
#     title: str
#     author: str

# @app.post("/books")
# async def create_book(book: BookCreateModel):
#     return {
#         "title": book.title,
#         "author": book.author
#     }

# @app.get("/headers")
# async def get_headers(accept: str= Header(None) , content_type: str = Header(None)):
#     req_headers = {}
#     req_headers["accept"] = accept
#     req_headers["content-type"] = content_type
#     return req_headers

books = [
    {
        "id": 1,
        "title": "Think Python",
        "author": "Allen B. Downey",
        "publisher": "O'Reilly Media",
        "published_date": "2021-01-01",
        "page_count": 1234,
        "language": "English",
    },
    {
        "id": 2,
        "title": "Django By Example",
        "author": "Antonio Mele",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2022-01-19",
        "page_count": 1023,
        "language": "English",
    },
    {
        "id": 3,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "publisher": "Prentice Hall",
        "published_date": "2008-08-11",
        "page_count": 464,
        "language": "English",
    },
    {
        "id": 4,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "publisher": "Addison-Wesley",
        "published_date": "1999-10-30",
        "page_count": 352,
        "language": "English",
    }
]

@app.get("/books")
async def get_all_books()->dict:
    return books

@app.get("/books")
async def get_a_book()->dict:
    pass

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int)->dict:
    for book in books:
        if book["id"] == book_id:
            return book
    return {"message": "Book not found"}

@app.post("/books")
async def create_book(book: dict)->dict:
    book["id"] = len(books) + 1
    books.append(book)
    return book

