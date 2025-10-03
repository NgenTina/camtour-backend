from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from .entity import EntityResponse
from .message import MessageResponse
from .user import UserResponse

if TYPE_CHECKING:
    from .user import UserResponse
    from .message import MessageResponse


class ConversationBase(BaseModel):
    title: str
    user_id: int


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    is_active: Optional[bool] = None


class ConversationResponse(ConversationBase):
    id: int
    is_active: bool
    user: Optional["UserResponse"] = None
    messages: List["MessageResponse"] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Resolve forward references
EntityResponse.update_forward_refs()
MessageResponse.update_forward_refs()
UserResponse.update_forward_refs()
ConversationResponse.update_forward_refs()
