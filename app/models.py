from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import text

from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, index=True, nullable=False)
    content: str = Column(String, index=True, nullable=False)
    is_published: bool = Column(Boolean, server_default='TRUE', nullable=False)
    rating: int = Column(Integer, default=0, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
