from sqlalchemy.orm import Session
from app.anc.database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from app.anc.schema import UserCreate, UserResponse
from app.anc.utils import hash_password
import app.anc.models as models
 
router = APIRouter(
    prefix = "/users",
    tags = ["Users",]
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = UserResponse)
def create_user(user: UserCreate,db: Session = Depends(get_db)):
    #hashing password using hash_password from utils.py

    user.password = hash_password(user.password)
    try:
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=f"Could not process the request.{e}")

@router.get("/{id}", response_model = UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user