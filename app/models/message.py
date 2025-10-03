from .conversation import Conversation
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey(
        "conversations.id"), nullable=False)
    sender_type = Column(String, nullable=False)  # Changed from Enum to String
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        onupdate=func.now(), server_default=func.now())

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    entities = relationship(
        "Entity", back_populates="message", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Message(id={self.id}, type='{self.sender_type}', content='{self.content[:50]}...')>"


# relationship to Conversation model (fk)
Conversation.messages = relationship(
    "Message", back_populates="conversation", cascade="all, delete-orphan")
