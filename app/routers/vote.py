from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from app.anc.database import get_db
from fastapi import status, HTTPException, Response, Depends, APIRouter
from app.anc.schema import UserResponse, VoteData
import app.anc.models as models
import app.anc.oauth2 as oauth2

router = APIRouter(
    prefix = "/vote",
    tags = ["Vote",]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: VoteData, current_user:UserResponse = Depends(oauth2.get_current_user), db: Session =  Depends(get_db)):
    
    post_id = vote.post_id
    post = db.query(models.Post).filter(models.Post.id==post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{post_id} does not exist")
    
    user_id = current_user.id

    voted_query = db.query(models.Vote).filter(models.Vote.user_id==user_id, models.Vote.post_id==post_id)
    voted = voted_query.first()

    if vote.dir==1:
        if voted:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {user_id} has already voted on post: {post_id}")
        new_vote = models.Vote(user_id=user_id, post_id=post_id)
        db.add(new_vote)
        db.commit()
        return f"Post: {post_id} liked by User: {user_id}"
    elif vote.dir==0:
        if not voted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with Id {user_id} has not voted on post id {post_id}")
        voted_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Sucessfully deleted vote"}