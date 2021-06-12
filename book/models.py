from typing import Optional, Union, Dict
import ormar
from datetime import datetime

from database.db import MainMeta

from user.models import User


class Book(ormar.Model):
    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=50)
    author: str = ormar.String(max_length=50)
    published: int = ormar.Integer()
    pages: int = ormar.Integer()
    create_at: datetime = ormar.DateTime(default=datetime.utcnow)
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name="user")

    class Meta(MainMeta):
        pass
