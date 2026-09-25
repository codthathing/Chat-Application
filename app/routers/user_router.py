from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session
import models
from app.schemas.user_schema import UserOut, UserDetailsOut, UserUsername, UserEmail
from typing import cast,List
from database import get_db
from app.utils.get_user_by_id import get_user_by_id


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get("/me/{user_id}", response_model=UserDetailsOut)
def get_user_details(user_id: UUID, db: Session = Depends(get_db)):
    friends = db.query(models.Friend).filter(models.Friend.u_id == user_id).all()
    groups = db.query(models.GroupMember).filter(models.GroupMember.u_id == user_id).all()

    friends_details = []
    for f in friends:
        friend = get_user_by_id(cast(UUID, cast(object, f.friend_id)), db)

        if friend:
            friends_details.append({"room_id": f.room_id, "id": friend.id, "username": friend.username})

    groups_details = []
    for g in groups:
        group = db.query(models.Group).filter(models.Group.id == g.group_id).first()

        if group:
            groups_details.append({"room_id": group.id, "group_name": group.group_name})

    return {"friends": friends_details, "groups": groups_details}

@router.patch("/username/{u_id}")
def update_username(user: UserUsername, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.id == user.u_id).first()

    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    user_model.username = user.username
    db.commit()

    return {"success": "Username updated"}

@router.patch("/email/{u_id}")
def update_email(user: UserEmail, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.id == user.u_id).first()

    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    user_model.email = user.email
    db.commit()

    return {"success": "Email updated"}