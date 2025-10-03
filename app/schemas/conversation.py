from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING


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
    # MessageResponse does NOT cause recursion
    messages: Optional[List["MessageResponse"]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
