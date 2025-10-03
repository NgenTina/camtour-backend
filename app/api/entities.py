from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.database import get_db
from app.models import Entity, Message
from app.schemas import EntityCreate, EntityUpdate, EntityResponse

router = APIRouter(prefix="/entities", tags=["entities"])

@router.post("/", response_model=EntityResponse)
async def create_entity(entity: EntityCreate, db: AsyncSession = Depends(get_db)):
    """Create a new entity"""
    # Verify message exists
    msg_result = await db.execute(select(Message).where(Message.id == entity.message_id))
    message = msg_result.scalars().first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    db_entity = Entity(**entity.model_dump())
    db.add(db_entity)
    await db.commit()
    await db.refresh(db_entity)
    return db_entity

@router.get("/{entity_id}", response_model=EntityResponse)
async def get_entity(entity_id: int, db: AsyncSession = Depends(get_db)):
    """Get entity by ID"""
    result = await db.execute(select(Entity).where(Entity.id == entity_id))
    entity = result.scalars().first()
    
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found"
        )
    
    return entity

@router.put("/{entity_id}", response_model=EntityResponse)
async def update_entity(
    entity_id: int, 
    entity_update: EntityUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """Update entity by ID"""
    result = await db.execute(select(Entity).where(Entity.id == entity_id))
    db_entity = result.scalars().first()
    
    if not db_entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found"
        )
    
    # Update entity fields
    for field, value in entity_update.model_dump(exclude_unset=True).items():
        setattr(db_entity, field, value)
    
    await db.commit()
    await db.refresh(db_entity)
    return db_entity

@router.delete("/{entity_id}")
async def delete_entity(entity_id: int, db: AsyncSession = Depends(get_db)):
    """Delete entity by ID"""
    result = await db.execute(select(Entity).where(Entity.id == entity_id))
    db_entity = result.scalars().first()
    
    if not db_entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found"
        )
    
    await db.delete(db_entity)
    await db.commit()
    return {"message": "Entity deleted successfully"}

@router.get("/", response_model=list[EntityResponse])
async def get_entities(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all entities with pagination"""
    result = await db.execute(
        select(Entity)
        .offset(skip)
        .limit(limit)
    )
    entities = result.scalars().all()
    return entities

@router.get("/message/{message_id}", response_model=list[EntityResponse])
async def get_message_entities(message_id: int, db: AsyncSession = Depends(get_db)):
    """Get all entities for a specific message"""
    result = await db.execute(
        select(Entity)
        .where(Entity.message_id == message_id)
    )
    entities = result.scalars().all()
    return entities

@router.get("/type/{entity_type}", response_model=list[EntityResponse])
async def get_entities_by_type(entity_type: str, db: AsyncSession = Depends(get_db)):
    """Get all entities of a specific type"""
    result = await db.execute(
        select(Entity)
        .where(Entity.entity_type == entity_type)
    )
    entities = result.scalars().all()
    return entities