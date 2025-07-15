from http.client import HTTPException
from typing import Optional

import psycopg2
from fastapi import FastAPI, HTTPException, Response
from fastapi.params import Depends
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from app import models
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "title of post 1", "content": "content of the post 1", "id": 1},
    {"title": "title of post 2", "content": "content of the post 2", "id": 2},
]

try:
    conn = psycopg2.connect(
        host='localhost',
        database='fastapi',
        user='postgres',
        password='admin',
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print("Connected to PostgreSQL")

except Exception as error:
    print("Connection to PostgreSQL failed")
    print("Error: ", error)


def get_last_id():
    return my_posts[-1].get("id", 0)


def find_post_by_id(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    raise HTTPException(status_code=404, detail="post not found")


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    try:
        posts = db.query(models.Post).all()
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQLAlchemy connection failed: {e}")


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT *
                      FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, is_published, rating)
           VALUES (%s, %s, %s, %s) RETURNING *""",
        (post.title, post.content, post.is_published, post.rating if post.rating is not None else 0,)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return new_post


@app.get("/posts/latest")
def get_latest_post():
    return my_posts[-1]


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts
                      SET title        = %s,
                          content      = %s,
                          is_published = %s,
                          rating       = %s
                      WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.is_published, post.rating, str(id),))
    post = cursor.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE
                      FROM posts
                      WHERE id = %s RETURNING *""", (str(id),))
    post = cursor.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT *
                      FROM posts
                      WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail=f"post {id} not found")
    return post
