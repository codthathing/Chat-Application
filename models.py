import uuid

from sqlalchemy import Column, String, UUID, Integer, Enum, UniqueConstraint, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    profile = Column(String, nullable=True)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)

class Room(Base):
    __tablename__ = "rooms"

    id = Column(UUID, primary_key=True, default=uuid.uuid4, index=True)
    room_name = Column(String, nullable=True)
    created_by = Column(UUID, ForeignKey('users.user_id'))

    __table_args__ = (UniqueConstraint('id', 'room_name', name='unique_room'),)

class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(UUID, ForeignKey('rooms.room_id'), index=True)
    friend_id = Column(UUID, index=True)
    u_id = Column(UUID, ForeignKey('users.user_id'), index=True)
    friend_firstname = Column(String, nullable=True)
    friend_lastname = Column(String, nullable=True)
    status = Enum("accepted", "declined", "pending")