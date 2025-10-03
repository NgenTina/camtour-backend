from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base

class Entity(Base):
    __tablename__ = "entities"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    entity_type = Column(String, nullable=False)  # e.g., "location", "activity", "time", "budget"
    entity_value = Column(String, nullable=False)
    confidence_score = Column(Integer, default=100)  # 0-100
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Relationships
    message = relationship("Message", back_populates="entities")
    
    def __repr__(self):
        return f"<Entity(id={self.id}, type='{self.entity_type}', value='{self.entity_value}')>"

# Add relationship to Message model
from .message import Message
Message.entities = relationship("Entity", back_populates="message", cascade="all, delete-orphan")