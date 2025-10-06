from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from app.database.database import get_db
from app.models import User, Conversation, Message
from app.schemas import UserCreate, UserUpdate, UserResponse, UserBasic

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user"""
    # Check if user already exists
    result = await db.execute(
        select(User).where((User.username == user.username)
                           | (User.email == user.email))
    )
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get user by ID with full details"""
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.conversations).options(
                selectinload(Conversation.messages).options(
                    selectinload(Message.entities)
                )
            )
        )
        .where(User.id == user_id)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    # Fetch the user with conversations eagerly loaded
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.conversations).selectinload(
                Conversation.messages)
        )
        .where(User.id == user_id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user fields
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    # Re-fetch with all relationships loaded for serialization
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.conversations).options(
                selectinload(Conversation.messages).options(
                    selectinload(Message.entities)
                )
            )
        )
        .where(User.id == user_id)
    )
    user = result.scalars().first()

    return UserResponse.model_validate(user)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Delete user by ID"""
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await db.delete(db_user)
    await db.commit()
    return {"message": "User deleted successfully"}


@router.get("/", response_model=list[UserResponse])
async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all users with pagination"""
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.conversations)
            .selectinload(Conversation.messages)
            .selectinload(Message.entities)
        )
        .offset(skip)
        .limit(limit)
    )
    users = result.scalars().all()
    return users
