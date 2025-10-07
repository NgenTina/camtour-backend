from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import users, conversations, messages, entities, auth

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Tourism Chatbot Backend API",
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(users.router, prefix=settings.api_v1_prefix)
app.include_router(conversations.router, prefix=settings.api_v1_prefix)
app.include_router(messages.router, prefix=settings.api_v1_prefix)
app.include_router(entities.router, prefix=settings.api_v1_prefix)
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get(f"{settings.api_v1_prefix}/")
async def root():
    return {
        "message": "Welcome to Tourism Chatbot Backend API",
        "version": "1.0.0",
        "endpoints": [
            f"{settings.api_v1_prefix}/users",
            f"{settings.api_v1_prefix}/conversations",
            f"{settings.api_v1_prefix}/messages",
            f"{settings.api_v1_prefix}/entities"
        ]
    }


@app.get(f"{settings.api_v1_prefix}/health")
async def health_check():
    return {"status": "healthy", "service": "tourism-chatbot-backend"}


@app.get(f"{settings.api_v1_prefix}/seed")
async def seed_database():
    """Development endpoint to reseed the database"""
    try:
        from seed_data import seed_data
        await seed_data()
        return {"message": "Database reseeded successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error seeding database: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
