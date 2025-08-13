from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import model, schema, utils

from ..database import engine, get_db


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schema.CreateUser
)
def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = model.UserModel(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schema.UserOut)
def get_user_by_email(id: int, db: Session = Depends(get_db)):
    user = db.query(model.UserModel).filter(model.UserModel.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with ID {id} does not exist",
        )
    return user