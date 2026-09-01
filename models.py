import uuid
from sqlalchemy import Column, String, UUID, Integer, Enum, UniqueConstraint, ForeignKey, DateTime
from database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    profile = Column(String, nullable=True)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)

class Room(Base):
    __tablename__ = "rooms"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    created_by = Column(UUID, ForeignKey('users.id'))
    type = Column(Enum("group", "user"))

class Group(Base):
    __tablename__ = "groups"

    id = Column(UUID, ForeignKey('rooms.id'), primary_key=True)
    group_profile = Column(String, nullable=True)
    group_name = Column(String)

class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True)
    group_id = Column(UUID, ForeignKey('groups.id'), index=True)
    u_id = Column(UUID, ForeignKey('users.id'), index=True)
    role = Column(Enum("admin", "member"), default="member")

    __table_args__ = (UniqueConstraint("group_id", "u_id", name="unique_member"),)

class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True)
    room_id = Column(UUID, ForeignKey('rooms.id'), index=True)
    friend_id = Column(UUID, ForeignKey('users.id'), index=True)
    u_id = Column(UUID, ForeignKey('users.id'), index=True)
    friend_firstname = Column(String, nullable=True)
    friend_lastname = Column(String, nullable=True)
    status = Column(Enum("accepted", "declined", "pending"), default="pending")

    __table_args__ = (UniqueConstraint("u_id", "friend_id", name="unique_friend_pair"),)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    room_id = Column(UUID, ForeignKey('rooms.id'), index=True)
    u_id = Column(UUID, ForeignKey('users.id'), index=True)
    text = Column(String)
    time_stamp = Column(DateTime, server_default=func.now())

class StatusContent(Base):
    __tablename__ = "status_contents"

    id = Column(UUID, ForeignKey('users.id'), primary_key=True)
    mime_type = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    storage_key = Column(String, nullable=True)