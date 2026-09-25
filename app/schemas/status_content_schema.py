from pydantic import BaseModel
from uuid import UUID

class StatusContent(BaseModel):
    u_id: UUID