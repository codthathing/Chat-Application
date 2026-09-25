from fastapi import APIRouter, Depends
import models
import bcrypt
from app.schemas.user_schema import User, UserOut
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=UserOut)
def create_account(user: User, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    user_model = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return user_model