from sqlalchemy.orm import Session
from app.anc.database import get_db
from fastapi import status, HTTPException, Response, Depends, APIRouter
from app.anc.schema import PostCreate, PostResponse, UserResponse, PostResponse_With_Votes
import app.anc.models as models, app.anc.oauth2 as oauth2
from sqlalchemy import func
from typing import List, Optional

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts",]
)

@router.get("/", response_model=List[PostResponse_With_Votes])
def get_posts(db: Session =  Depends(get_db), current_user: UserResponse = Depends(oauth2.get_current_user), Limit:int = 10, skip=0, search: Optional[str] = ""):
    # cur.execute("SELECT * FROM posts;")
    # posts_all=cur.fetchall()
    #posts_all = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).all()
    return posts

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session =  Depends(get_db), current_user: UserResponse = Depends(oauth2.get_current_user)):
    try:
        # cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
        # new_post=cur.fetchone()
        # conn.commit()
        owner_id = current_user.id
        new_post = models.Post(**post.dict())
        new_post.owner_id = owner_id
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=f"Could not process the request")
        
@router.get("/{id}", response_model=PostResponse_With_Votes)
def get_post(id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(oauth2.get_current_user)):
    #cur.execute("""SELECT * FROM posts WHERE id=%s""",(id,))
    #selected_post=cur.fetchone()
    #selected_post = db.query(models.Post).filter(models.Post.id==id).first()
    selected_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if selected_post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"The requested post with id {id} does not exist")
    return selected_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(oauth2.get_current_user)):
    # cur.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(id,))
    # post_status=cur.fetchone()
    # conn.commit()
    post_status =  db.query(models.Post).filter(models.Post.id==id)
    if post_status.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"The requested post with id {id} does not exist")
    
    if not post_status.first().owner_id == current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not Authorized")

    post_status.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
           
@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(oauth2.get_current_user)):
    # cur.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.published, id))
    # conn.commit()
        
    post_query = db.query(models.Post).filter(models.Post.id==id)
    if post_query.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Could not process the request")
    
    if not post_query.first().owner_id == current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not Authorized")
    post.owner_id = post_query.first().owner_id
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
