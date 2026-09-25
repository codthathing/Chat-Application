from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from app.schemas.friend_schema import FriendOut
from app.schemas.group_schema import GroupOut

class User(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    email: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=1, max_length=15)

class UserUsername(BaseModel):
    username: str
    u_id: UUID

class UserEmail(BaseModel):
    email: str
    u_id: UUID

class UserOut(BaseModel):
    id: UUID
    username: str
    email: str
    profile: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    model_config = ConfigDict(from_attributes=True)

class UserDetailsOut(BaseModel):
    friends: list[FriendOut]
    groups: list[GroupOut]