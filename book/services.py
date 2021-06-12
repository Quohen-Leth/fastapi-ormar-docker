from fastapi import HTTPException

from . import models, schemas


async def save_book(
        user: models.User,
        title: str,
        author: str,
        published: int,
        pages: int
):
    info = schemas.UploadBook(
        title=title,
        author=author,
        published=published,
        pages=pages
    )
    return await models.Book.objects.create(user=user.dict(), **info.dict())


async def get_book(book_id: int, user_pk: str):
    book = await models.Book.objects.get_or_none(id=book_id, user=user_pk)
    if not book:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return book
