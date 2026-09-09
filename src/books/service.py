from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import BookCreateModel, BookUpdateModel
from src.books.models import Book
from sqlalchemy import select, update, delete, desc
from datetime import datetime

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.scalars().all()

    async def get_book(self, book_id: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_id)
        result = await session.exec(statement)
        return result.scalars().first()

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)

        new_book.published_date = datetime.strftime(book_data_dict["published_date"] , "%Y-%m-%d")

        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)  # Refreshes model to get DB-generated fields like uid/created_at
        return new_book

    async def update_book(self, book_id: str, update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book(book_id, session)

        if book_to_update:
            update_data_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_data_dict.items():
                setattr(book_to_update, key, value)

            await session.commit()
            await session.refresh(book_to_update)
            return book_to_update
        
        return None

    async def delete_book(self, book_id: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_id, session)

        if book_to_delete:
            await session.delete(book_to_delete)
            await session.commit()
            return True  # Returning True or the deleted object is standard for status checks

        return None