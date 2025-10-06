from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .conversation import ConversationResponse


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserBasic(UserBase):
    id: int
    is_active: Optional[bool] = True


class UserResponse(UserBase):
    id: int
    username: str
    email: str
    is_active: Optional[bool] = True
    conversations: Optional[List["ConversationResponse"]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True
