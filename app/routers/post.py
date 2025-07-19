from typing import List, Optional

from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db
from app.oauth2 import get_current_user
from app.schemas import UserResponse

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("", response_model=List[schemas.PostVoteResponse])
def get_posts(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user),
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        search: Optional[str] = ""):
    query = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
    )

    if search:
        query = query.filter(models.Post.title.contains(search))

    if limit:
        query = query.limit(limit)

    if skip:
        query = query.offset(skip)

    posts = query.all()
    return posts


@router.get("/my_posts", response_model=List[schemas.PostResponse])
def get_my_posts(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    if not posts:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return posts


@router.get("/latest", response_model=schemas.PostResponse)
def get_latest_post(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    if not post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
    return post


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: UserResponse = Depends(get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db),
                current_user: UserResponse = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado para realizar essa ação")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} não encontrado")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado para realizar essa ação")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
