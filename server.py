from fastapi import FastAPI, HTTPException, Depends
from pydantic import Field, BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class User(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    email: str = Field(min_length=1, max_length=30)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"users": db.query(models.User).all()}


@app.post("/users")
def upload_user(user: User, db: Session = Depends(get_db)):
    user_model = models.User(username=user.username, email=user.email)
    db.add(user_model)
    db.commit()

    return user