from pydantic import BaseModel
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .message import MessageResponse


class EntityBase(BaseModel):
    message_id: int
    entity_type: str
    entity_value: str
    confidence_score: Optional[int] = 100


class EntityCreate(EntityBase):
    pass


class EntityUpdate(BaseModel):
    entity_type: Optional[str] = None
    entity_value: Optional[str] = None
    confidence_score: Optional[int] = None


class EntityResponse(EntityBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Do NOT include message: MessageResponse here to avoid recursion

    class Config:
        from_attributes = True


# Resolve forward references
