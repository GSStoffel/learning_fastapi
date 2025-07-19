from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, index=True, nullable=False)
    content: str = Column(String, index=True, nullable=False)
    is_published: bool = Column(Boolean, server_default='TRUE', nullable=False)
    rating: int = Column(Integer, default=0, nullable=True)
    created_at: datetime = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, nullable=False, unique=True)
    password: str = Column(String, nullable=False)
    create_at: datetime = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)


class Vote(Base):
    __tablename__ = "votes"

    user_id: int = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id: int = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)