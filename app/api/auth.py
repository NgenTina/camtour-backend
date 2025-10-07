from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.database import get_db
from app.models import User
from app.schemas.user import UserCreate, UserResponse
from app.core.auth import (
    create_access_token, get_password_hash, verify_password, get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.core.config import settings

router = APIRouter(tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login")


async def authenticate_user(db: AsyncSession, username: str, password: str):
    """Authenticate a user by username and password"""
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalars().first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
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

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """Login and get access token"""
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(db: AsyncSession = Depends(get_db)):
    """Get current user information - TEMPORARILY DISABLED AUTH"""
    # For now, return the first user as a placeholder
    result = await db.execute(select(User).limit(1))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="No users found")
    return user
