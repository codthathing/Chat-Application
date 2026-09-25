from uuid import UUID
from pydantic import BaseModel
from typing import Literal

class GroupMember(BaseModel):
    u_id: UUID
    group_id: UUID

class GroupMemberUpdate(BaseModel):
    u_id: UUID
    group_id: UUID
    role: Literal["admin", "member"] | None = None