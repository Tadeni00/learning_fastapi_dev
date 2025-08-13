from ctypes import util
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import model, schema, utils, database, oauth2


router = APIRouter(
    prefix="/login",
    tags=["auth"]
)

@router.post("/", response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    db_user = db.query(model.UserModel).filter(model.UserModel.email == user_credentials.username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    # Ensure you are passing the actual password string, not the SQLAlchemy Column object
    if not utils.verify(user_credentials.password, getattr(db_user, "password")):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    
    access_token = oauth2.create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    