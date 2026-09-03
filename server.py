from uuid import UUID
from fastapi import FastAPI, HTTPException, Depends
from pydantic import Field, BaseModel, ConfigDict
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import bcrypt
from typing import List, cast


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class User(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    email: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=1, max_length=15)

class UserOut(BaseModel):
    id: UUID
    username: str
    email: str
    profile: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    model_config = ConfigDict(from_attributes=True)

class FriendOut(BaseModel):
    room_id: UUID
    id: UUID
    username: str
    model_config = ConfigDict(from_attributes=True)

# class GroupMemberOut(BaseModel):
#     id: UUID
#     username: str
#     email: str
#     role: str
#     model_config = ConfigDict(from_attributes=True)

class GroupOut(BaseModel):
    room_id: UUID
    group_name: str
    model_config = ConfigDict(from_attributes=True)

class UserDetailsOut(BaseModel):
    friends: list[FriendOut]
    groups: list[GroupOut]

class AddFriendRequest(BaseModel):
    u_id: UUID
    friend_id: UUID

class Group(BaseModel):
    group_name: str = Field(min_length=1, max_length=20)
    u_id: UUID

class GroupMember(BaseModel):
    u_id: UUID
    group_id: UUID

class Message(BaseModel):
    room_id: UUID
    u_id: UUID
    text: str

class StatusContent(BaseModel):
    u_id: UUID


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.id == user_id).first()


@app.get("/users/me/{user_id}", response_model=UserDetailsOut)
def get_user_details(user_id: UUID, db: Session = Depends(get_db)):
    friends = db.query(models.Friend).filter(models.Friend.u_id == user_id).all()
    groups = db.query(models.GroupMember).filter(models.GroupMember.u_id == user_id).all()

    friends_details = []
    for f in friends:
        friend = get_user(cast(UUID, cast(object, f.friend_id)), db)

        if friend:
            friends_details.append({"room_id": f.room_id, "id": friend.id, "username": friend.username})

    groups_details = []
    for g in groups:
        group = db.query(models.Group).filter(models.Group.id == g.group_id).first()

        if group:
            groups_details.append({"room_id": group.id, "group_name": group.group_name})

    return {"friends": friends_details, "groups": groups_details}


@app.post("/users", response_model=UserOut)
def upload_user(user: User, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    user_model = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return user_model


@app.get("/friends")
def get_friends(db: Session = Depends(get_db)):
    return db.query(models.Friend).all()


@app.post("/friends")
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


@app.get("/groups")
def get_groups(db: Session = Depends(get_db)):
    return db.query(models.Group).all()


@app.post("/groups")
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


@app.get("/group-members")
def get_group_members(db: Session = Depends(get_db)):
    return db.query(models.GroupMember).all()


@app.post("/group-members")
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
    db.refresh(group_member)

    return group_member


@app.post("/messages")
def add_message(message: Message, db: Session = Depends(get_db)):
    message = models.Message(room_id=message.room_id, u_id=message.u_id, text=message.text)
    db.add(message)
    db.commit()
    db.refresh(message)

    return message


@app.post("/status-contents")
def upload_status(status_content: StatusContent, db: Session = Depends(get_db)):
    status_content = models.StatusContent(id=status_content.u_id)
    db.add(status_content)
    db.commit()
    db.refresh(status_content)

    return status_content