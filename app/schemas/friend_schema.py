from pydantic import BaseModel, ConfigDict
from uuid import UUID

class FriendOut(BaseModel):
    room_id: UUID
    id: UUID
    username: str
    model_config = ConfigDict(from_attributes=True)

class AddFriendRequest(BaseModel):
    u_id: UUID
    friend_id: UUID