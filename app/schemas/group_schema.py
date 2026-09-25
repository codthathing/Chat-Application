from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

class Group(BaseModel):
    group_name: str = Field(min_length=1, max_length=20)
    u_id: UUID

class GroupOut(BaseModel):
    room_id: UUID
    group_name: str
    model_config = ConfigDict(from_attributes=True)