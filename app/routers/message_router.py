from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
from database import get_db
from typing import cast
from uuid import UUID
from app.schemas.message_schema import Message
from app.utils.get_user_by_id import get_user_by_id


router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("")
def get_messages(db: Session = Depends(get_db)):
    return db.query(models.Message).all()


@router.post("")
def add_message(message: Message, db: Session = Depends(get_db)):
    message = models.Message(room_id=message.room_id, u_id=message.u_id, text=message.text)
    db.add(message)
    db.commit()
    db.refresh(message)

    return message


@router.get("/{room_id}")
def get_room_messages(room_id: UUID, db: Session = Depends(get_db)):
    messages_details = db.query(models.Message).filter(models.Message.room_id == room_id).all()

    messages = []

    for m in messages_details:
        user = get_user_by_id(cast(UUID, cast(object, m.u_id)), db)

        if user:
            messages.append({"username": user.username, "text": m.text, "time_stamp": m.time_stamp})

    return messages