from .entity import EntityCreate, EntityUpdate, EntityResponse
from .message import MessageCreate, MessageUpdate, MessageResponse
from .user import UserCreate, UserUpdate, UserResponse, UserBasic
from .conversation import ConversationCreate, ConversationUpdate, ConversationResponse


__all__ = [
    "UserCreate", "UserUpdate", "UserResponse", "UserBasic",
    "ConversationCreate", "ConversationUpdate", "ConversationResponse",
    "MessageCreate", "MessageUpdate", "MessageResponse",
    "EntityCreate", "EntityUpdate", "EntityResponse"
]

# Rebuild models and update forward refs to resolve circular/forward references
UserResponse.model_rebuild()
ConversationResponse.model_rebuild()
MessageResponse.model_rebuild()
EntityResponse.model_rebuild()
UserResponse.update_forward_refs()
ConversationResponse.update_forward_refs()
MessageResponse.update_forward_refs()
EntityResponse.update_forward_refs()
