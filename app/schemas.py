from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
