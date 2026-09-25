from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
from database import get_db
from app.schemas.group_schema import Group


router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("")
def get_groups(db: Session = Depends(get_db)):
    return db.query(models.Group).all()


@router.post("")
def create_group(group: Group, db: Session = Depends(get_db)):
    room = models.Room(created_by=group.u_id, type="group")
    db.add(room)
    db.flush()

    group_obj = models.Group(id=room.id, group_name=group.group_name)
    db.add(group_obj)

    group_member = models.GroupMember(group_id=group_obj.id, u_id=group.u_id, role="admin")
    db.add(group_member)

    db.commit()
    db.refresh(group_obj)
    db.refresh(group_member)

    return {"group": group_obj, "membership": group_member}