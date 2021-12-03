from fastapi import APIRouter, Depends,  HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.anc.schema import Token
from app.anc.database import get_db
from sqlalchemy.orm import Session
import app.anc.models as models
from app.anc.utils import verify
from app.anc.oauth2 import create_access_token

router = APIRouter(
    tags = ["Authentication", ]
    )

@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #OAuth2PasswordRequestForm has two fields namely username and password. Thus, even though we are fetching users's email from the database, we still need to compare it with username field of the user_credentials object
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
