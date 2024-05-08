from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from ..models import Todos, Users
from typing import Annotated
from pydantic import BaseModel, Field
from ..database import SessionLocal
from .auth import get_current_user
from .auth import hash_password, verify_password


router = APIRouter(prefix="/user", tags=["user"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)





@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not user_model:
        raise HTTPException(status_code=404, detail='User not found')
    return {
        'id': user_model.id,
        'username': user_model.username,
        'email': user_model.email,
        'first_name': user_model.first_name,
        'last_name': user_model.last_name,
        'role': user_model.role,
        'is_active': user_model.is_active,
        'phone_number': user_model.phone_number
    }



@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    user_model = db.query(Users).filter(Users.id == user['id']).first()

    if not verify_password(user_verification.password, bytes(user_model.hashed_password)):
        raise HTTPException(status_code=401, detail='Error on password change')

    # Hash the new password
    new_hashed_password = hash_password(user_verification.new_password)

    # Update the hashed password in the user model
    user_model.hashed_password = new_hashed_password

    db.add(user_model)
    db.commit()


@router.put('/phonenumber/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
