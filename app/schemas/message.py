from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .entity import EntityResponse
    from .conversation import ConversationResponse


class MessageBase(BaseModel):
    conversation_id: int
    sender_type: str
    content: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    content: Optional[str] = None


class MessageResponse(MessageBase):
    id: int
    created_at: datetime
    entities: Optional[List["EntityResponse"]] = None

    class Config:
        from_attributes = True


# Resolve forward references
