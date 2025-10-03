from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.database import get_db
from app.models import Message, Conversation
from app.schemas import MessageCreate, MessageUpdate, MessageResponse

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=MessageResponse)
async def create_message(message: MessageCreate, db: AsyncSession = Depends(get_db)):
    """Create a new message"""
    # Verify conversation exists
    conv_result = await db.execute(select(Conversation).where(Conversation.id == message.conversation_id))
    conversation = conv_result.scalars().first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    db_message = Message(**message.model_dump())
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message

@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(message_id: int, db: AsyncSession = Depends(get_db)):
    """Get message by ID"""
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalars().first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    return message

@router.put("/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: int, 
    message_update: MessageUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """Update message by ID"""
    result = await db.execute(select(Message).where(Message.id == message_id))
    db_message = result.scalars().first()
    
    if not db_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Update message fields
    for field, value in message_update.model_dump(exclude_unset=True).items():
        setattr(db_message, field, value)
    
    await db.commit()
    await db.refresh(db_message)
    return db_message

@router.delete("/{message_id}")
async def delete_message(message_id: int, db: AsyncSession = Depends(get_db)):
    """Delete message by ID"""
    result = await db.execute(select(Message).where(Message.id == message_id))
    db_message = result.scalars().first()
    
    if not db_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    await db.delete(db_message)
    await db.commit()
    return {"message": "Message deleted successfully"}

@router.get("/", response_model=list[MessageResponse])
async def get_messages(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all messages with pagination"""
    result = await db.execute(
        select(Message)
        .offset(skip)
        .limit(limit)
    )
    messages = result.scalars().all()
    return messages

@router.get("/conversation/{conversation_id}", response_model=list[MessageResponse])
async def get_conversation_messages(conversation_id: int, db: AsyncSession = Depends(get_db)):
    """Get all messages for a specific conversation"""
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    messages = result.scalars().all()
    return messages