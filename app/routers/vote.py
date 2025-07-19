from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.oauth2 import get_current_user
from app.schemas import UserResponse, VoteBase

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("", status_code=status.HTTP_200_OK)
def vote(vote: VoteBase, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} não encontrado")

    existing_vote = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                                 models.Vote.user_id == current_user.id).first()

    if existing_vote:
        db.delete(existing_vote)
        db.commit()
        return {"message": f"Voto removido para o post {vote.post_id}"}
    else:
        db.add(models.Vote(user_id=current_user.id, post_id=vote.post_id))
        db.commit()
        return {"message": f"Voto concedido para o post {vote.post_id}"}
