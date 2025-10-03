from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.database import get_db
from app.models import Conversation, User
from app.schemas import ConversationCreate, ConversationUpdate, ConversationResponse

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("/", response_model=ConversationResponse)
async def create_conversation(conversation: ConversationCreate, db: AsyncSession = Depends(get_db)):
    """Create a new conversation"""
    # Verify user exists
    user_result = await db.execute(select(User).where(User.id == conversation.user_id))
    user = user_result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db_conversation = Conversation(**conversation.model_dump())
    db.add(db_conversation)
    await db.commit()
    await db.refresh(db_conversation)
    return db_conversation

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: int, db: AsyncSession = Depends(get_db)):
    """Get conversation by ID"""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.id == conversation_id)
    )
    conversation = result.scalars().first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return conversation

@router.put("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: int, 
    conversation_update: ConversationUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """Update conversation by ID"""
    result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
    db_conversation = result.scalars().first()
    
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Update conversation fields
    for field, value in conversation_update.model_dump(exclude_unset=True).items():
        setattr(db_conversation, field, value)
    
    await db.commit()
    await db.refresh(db_conversation)
    return db_conversation

@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: int, db: AsyncSession = Depends(get_db)):
    """Delete conversation by ID"""
    result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
    db_conversation = result.scalars().first()
    
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    await db.delete(db_conversation)
    await db.commit()
    return {"message": "Conversation deleted successfully"}

@router.get("/", response_model=list[ConversationResponse])
async def get_conversations(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all conversations with pagination"""
    result = await db.execute(
        select(Conversation)
        .offset(skip)
        .limit(limit)
    )
    conversations = result.scalars().all()
    return conversations

@router.get("/user/{user_id}", response_model=list[ConversationResponse])
async def get_user_conversations(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get all conversations for a specific user"""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
    )
    conversations = result.scalars().all()
    return conversations