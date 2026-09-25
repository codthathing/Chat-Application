from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db
from app.schemas.friend_schema import AddFriendRequest


router = APIRouter(prefix="/friends", tags=["friends"])


@router.get("")
def get_friends(db: Session = Depends(get_db)):
    return db.query(models.Friend).all()


@router.post("")
def add_friend(request: AddFriendRequest, db: Session = Depends(get_db)):
    if request.u_id == request.friend_id:
        raise HTTPException(status_code=400, detail="Cannot send a friend request to yourself")

    existing = db.query(models.Friend).filter(models.Friend.u_id == request.u_id, models.Friend.friend_id == request.friend_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Friend request already exists")

    room = models.Room(created_by=request.u_id, type="user")
    db.add(room)
    db.flush()

    friend_one = models.Friend(room_id=room.id, friend_id=request.friend_id, u_id=request.u_id)
    friend_two = models.Friend(room_id=room.id, friend_id=request.u_id, u_id=request.friend_id)
    db.add_all([friend_one, friend_two])

    db.commit()
    db.refresh(friend_one)

    return friend_one