from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db
from app.schemas.group_member_schema import GroupMember, GroupMemberUpdate
from uuid import UUID
from typing import cast
from app.utils.get_user_by_id import get_user_by_id


router = APIRouter(prefix="/group-members", tags=["Group Members"])


@router.get("")
def get_groups_members(db: Session = Depends(get_db)):
    return db.query(models.GroupMember).all()


@router.post("")
def create_group_member(group: GroupMember, db: Session = Depends(get_db)):
    group_exists = db.query(models.Group).filter(models.Group.id == group.group_id).first()
    if not group_exists:
        raise HTTPException(status_code=404, detail="Group not found")

    user_exists = db.query(models.User).filter(models.User.id == group.u_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    existing = db.query(models.GroupMember).filter(models.GroupMember.group_id == group.group_id, models.GroupMember.u_id == group.u_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Group member already exists")

    group_member = models.GroupMember(group_id=group.group_id, u_id=group.u_id)

    db.add(group_member)
    db.commit()

    return {"success": "New user added to group!"}


@router.patch("/{group_id}/{u_id}")
def update_group_member_status(group: GroupMemberUpdate, db: Session = Depends(get_db)):
    group_member = db.query(models.GroupMember).filter(models.GroupMember.group_id == group.group_id, models.GroupMember.u_id == group.u_id).first()

    if not group_member:
        raise HTTPException(status_code=404, detail="Group not found")

    group_member.role = group.role or "member"
    db.commit()

    return {"success": "New admin added!"}



@router.get("/{group_id}")
def get_group_members(group_id: UUID, db: Session = Depends(get_db)):
    members_details = db.query(models.GroupMember).filter(models.GroupMember.group_id == group_id).all()

    members = []

    for m in members_details:
        user = get_user_by_id(cast(UUID, cast(object, m.u_id)), db)

        if user:
            members.append({"id": user.id, "username": user.username, "email": user.email, "role": m.role})

    return members