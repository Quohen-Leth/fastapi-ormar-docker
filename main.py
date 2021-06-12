from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from database.db import database  # , metadata, engine
from book.api import book_router
from user.routers import user_router

app = FastAPI(title="Bookshelf API", description="Simple api to save favorite books", version="0.1.0")

# metadata.create_all(engine)  # первинна ініціалізація бази
app.state.database = database  # підключення бази

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(user_router)
app.include_router(book_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
