from pydantic import BaseModel
from uuid import UUID

class Message(BaseModel):
    room_id: UUID
    u_id: UUID
    text: str