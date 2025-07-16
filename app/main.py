import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from app import models
from app.database import engine
from app.routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
