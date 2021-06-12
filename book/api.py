from typing import List, Optional
from starlette.requests import Request
from fastapi import APIRouter, Form, Depends
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from user.auth import current_active_user
from . import models, schemas, services

book_router = APIRouter(tags=['book'])
templates = Jinja2Templates(directory="templates")


@book_router.post("/books/", status_code=201)
async def create_book(
        title: str = Form(...),
        author: str = Form(...),
        published: int = Form(...),
        pages: int = Form(...),
        user: models.User = Depends(current_active_user)
):
    return await services.save_book(user, title, author, published, pages)


@book_router.get("/books/", response_class=HTMLResponse)
async def get_book(
    request: Request,
    title: Optional[str] = "",
    author: Optional[str] = "",
    minyear: Optional[int] = -3000,  # For the case, if someone would like to add mesopotamian clay tablets.
    maxyear: Optional[int] = 9999  # To avoid import datetime for now()
):
    books = await models.Book.objects.select_related("user").filter(
        models.Book.title.icontains(title),
        models.Book.author.icontains(author),
        (models.Book.published >= minyear) & (models.Book.published <= maxyear)
    ).all()

    return templates.TemplateResponse("books.html", {"request": request, "books": books})


@book_router.get("/books/me/", response_model=List[schemas.GetListBook])
async def get_list_book(user: models.User = Depends(current_active_user)):
    return await models.Book.objects.filter(user=user.id).all()


@book_router.get("/books/me/{book_id}", response_model=schemas.GetListBook)
async def get_my_book(book_id: int, user: models.User = Depends(current_active_user)):
    return await services.get_book(book_id, user.id)


@book_router.put("/books/me/{book_id}", response_model=schemas.GetListBook)
async def update_book(
    book_id: int,
    book_flds: schemas.UpdateBook,
    user: models.User = Depends(current_active_user)
):
    book = await services.get_book(book_id, user.id)
    return await book.update(**book_flds.dict(exclude_none=True))


@book_router.delete("/books/me/{book_id}", status_code=204)
async def delete_book(book_id: int, user: models.User = Depends(current_active_user)):
    book = await services.get_book(book_id, user.id)
    return await book.delete()
