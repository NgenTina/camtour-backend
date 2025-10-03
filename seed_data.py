import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from app.models import User, Conversation, Message, Entity
from app.database.database import Base
from app.core.config import settings

# Update the database URL to use the ephemeral database credentials
settings.database_url = "postgresql+asyncpg://ephemeral_user:ephemeral_pass@localhost:5433/ephemeral_db"

print(f"Using database URL: {settings.database_url}")

# Create async engine for seeding
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False
)


async def test_connection():
    """Test the database connection"""
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("Database connection successful!")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


async def drop_and_create_tables():
    """Drop all tables and recreate them"""
    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def seed_data():
    """Seed the database with sample data for testing"""

    # Test connection first
    if not await test_connection():
        raise Exception("Cannot connect to database")

    # Drop and recreate tables
    await drop_and_create_tables()

    async with AsyncSessionLocal() as session:
        print("Creating sample users...")

        # Create sample users
        users_data = [
            {
                "username": "tourist_john",
                "email": "john@example.com",
                "full_name": "John Doe"
            },
            {
                "username": "traveler_jane",
                "email": "jane@example.com",
                "full_name": "Jane Smith"
            },
            {
                "username": "adventure_mike",
                "email": "mike@example.com",
                "full_name": "Mike Johnson"
            }
        ]

        users = []
        for user_data in users_data:
            user = User(**user_data)
            session.add(user)
            users.append(user)

        await session.commit()
        print(f"Created {len(users)} users")

        print("Creating sample conversations...")

        # Create sample conversations
        conversations_data = [
            {
                "title": "Planning Trip to Paris",
                "user_id": users[0].id
            },
            {
                "title": "Beach Vacation in Bali",
                "user_id": users[1].id
            },
            {
                "title": "Mountain Hiking in Switzerland",
                "user_id": users[2].id
            },
            {
                "title": "City Tour in Tokyo",
                "user_id": users[0].id
            }
        ]

        conversations = []
        for conv_data in conversations_data:
            conversation = Conversation(**conv_data)
            session.add(conversation)
            conversations.append(conversation)

        await session.commit()
        print(f"Created {len(conversations)} conversations")

        print("Creating sample messages...")

        # Create sample messages with realistic tourism conversations
        messages_data = [
            # Conversation 1 - Paris trip
            {
                "conversation_id": conversations[0].id,
                "sender_type": "user",
                "content": "I want to plan a trip to Paris. What are the must-see attractions?"
            },
            {
                "conversation_id": conversations[0].id,
                "sender_type": "ai",
                "content": "Paris has many amazing attractions! The Eiffel Tower, Louvre Museum, Notre-Dame Cathedral, and Montmartre are must-see places."
            },
            {
                "conversation_id": conversations[0].id,
                "sender_type": "user",
                "content": "When is the best time to visit Paris?"
            },
            {
                "conversation_id": conversations[0].id,
                "sender_type": "ai",
                "content": "The best time to visit Paris is during spring (April-June) or fall (September-November) when the weather is pleasant and crowds are smaller."
            },
            {
                "conversation_id": conversations[0].id,
                "sender_type": "user",
                "content": "How much should I budget for a 5-day trip to Paris?"
            },
            {
                "conversation_id": conversations[0].id,
                "sender_type": "ai",
                "content": "For a 5-day trip to Paris, budget around $100-150 per day for mid-range accommodation, meals, and attractions. Total: $500-750."
            },

            # Conversation 2 - Bali trip
            {
                "conversation_id": conversations[1].id,
                "sender_type": "user",
                "content": "I'm planning a beach vacation in Bali. What are the best beaches?"
            },
            {
                "conversation_id": conversations[1].id,
                "sender_type": "ai",
                "content": "Bali has beautiful beaches! Kuta Beach, Seminyak Beach, Nusa Dua Beach, and Padang Padang Beach are among the best."
            },
            {
                "conversation_id": conversations[1].id,
                "sender_type": "user",
                "content": "What's the weather like in Bali in December?"
            },
            {
                "conversation_id": conversations[1].id,
                "sender_type": "ai",
                "content": "December in Bali is during the wet season with occasional heavy rains, but it's still warm with temperatures around 27-30°C. It's also the holiday season."
            },

            # Conversation 3 - Switzerland hiking
            {
                "conversation_id": conversations[2].id,
                "sender_type": "user",
                "content": "I want to go mountain hiking in Switzerland. What are the best trails?"
            },
            {
                "conversation_id": conversations[2].id,
                "sender_type": "ai",
                "content": "Switzerland has amazing hiking trails! The Eiger Trail, Matterhorn Trail, and the Haute Route are popular among hikers. Consider the Swiss National Park for easier trails."
            },
            {
                "conversation_id": conversations[2].id,
                "sender_type": "user",
                "content": "What equipment do I need for hiking in the Swiss Alps?"
            },
            {
                "conversation_id": conversations[2].id,
                "sender_type": "ai",
                "content": "For Swiss Alps hiking, you'll need good hiking boots, layered clothing, rain gear, a hat, sunglasses, sunscreen, a backpack with water and snacks, and a detailed map or GPS device."
            },

            # Conversation 4 - Tokyo city tour
            {
                "conversation_id": conversations[3].id,
                "sender_type": "user",
                "content": "I'm planning a city tour in Tokyo. What are the must-visit districts?"
            },
            {
                "conversation_id": conversations[3].id,
                "sender_type": "ai",
                "content": "Tokyo has amazing districts! Shibuya for shopping and nightlife, Shinjuku for skyscrapers and entertainment, Asakusa for traditional culture, and Harajuku for youth culture and fashion."
            },
            {
                "conversation_id": conversations[3].id,
                "sender_type": "user",
                "content": "How do I get around Tokyo efficiently?"
            },
            {
                "conversation_id": conversations[3].id,
                "sender_type": "ai",
                "content": "Tokyo has an excellent public transportation system. Get a Suica or Pasmo card for trains and buses. The subway system is extensive and connects most major attractions efficiently."
            }
        ]

        messages = []
        for msg_data in messages_data:
            message = Message(**msg_data)
            session.add(message)
            messages.append(message)

        await session.commit()
        print(f"Created {len(messages)} messages")

        print("Creating sample entities...")

        # Create sample entities to demonstrate entity extraction
        entities_data = [
            # Entities for Paris conversation
            {"message_id": messages[0].id, "entity_type": "location",
                "entity_value": "Paris", "confidence_score": 100},
            {"message_id": messages[0].id, "entity_type": "attraction",
                "entity_value": "Eiffel Tower", "confidence_score": 95},
            {"message_id": messages[0].id, "entity_type": "attraction",
                "entity_value": "Louvre Museum", "confidence_score": 95},
            {"message_id": messages[2].id, "entity_type": "time",
                "entity_value": "best time to visit", "confidence_score": 90},
            {"message_id": messages[4].id, "entity_type": "time",
                "entity_value": "5-day trip", "confidence_score": 85},
            {"message_id": messages[4].id, "entity_type": "location",
                "entity_value": "Paris", "confidence_score": 100},
            {"message_id": messages[4].id, "entity_type": "budget",
                "entity_value": "$500-750", "confidence_score": 90},

            # Entities for Bali conversation
            {"message_id": messages[6].id, "entity_type": "location",
                "entity_value": "Bali", "confidence_score": 100},
            {"message_id": messages[6].id, "entity_type": "activity",
                "entity_value": "beach vacation", "confidence_score": 95},
            {"message_id": messages[6].id, "entity_type": "attraction",
                "entity_value": "Kuta Beach", "confidence_score": 90},
            {"message_id": messages[6].id, "entity_type": "attraction",
                "entity_value": "Seminyak Beach", "confidence_score": 90},
            {"message_id": messages[8].id, "entity_type": "time",
                "entity_value": "December", "confidence_score": 95},
            {"message_id": messages[8].id, "entity_type": "weather",
                "entity_value": "wet season", "confidence_score": 85},

            # Entities for Switzerland hiking
            {"message_id": messages[10].id, "entity_type": "location",
                "entity_value": "Switzerland", "confidence_score": 100},
            {"message_id": messages[10].id, "entity_type": "activity",
                "entity_value": "mountain hiking", "confidence_score": 95},
            {"message_id": messages[10].id, "entity_type": "attraction",
                "entity_value": "Eiger Trail", "confidence_score": 90},
            {"message_id": messages[10].id, "entity_type": "attraction",
                "entity_value": "Matterhorn Trail", "confidence_score": 90},
            {"message_id": messages[12].id, "entity_type": "activity",
                "entity_value": "hiking", "confidence_score": 95},
            {"message_id": messages[12].id, "entity_type": "location",
                "entity_value": "Swiss Alps", "confidence_score": 95},

            # Entities for Tokyo city tour
            {"message_id": messages[14].id, "entity_type": "location",
                "entity_value": "Tokyo", "confidence_score": 100},
            {"message_id": messages[14].id, "entity_type": "activity",
                "entity_value": "city tour", "confidence_score": 90},
            {"message_id": messages[14].id, "entity_type": "attraction",
                "entity_value": "Shibuya", "confidence_score": 95},
            {"message_id": messages[14].id, "entity_type": "attraction",
                "entity_value": "Shinjuku", "confidence_score": 95},
            {"message_id": messages[16].id, "entity_type": "activity",
                "entity_value": "get around", "confidence_score": 85},
            {"message_id": messages[16].id, "entity_type": "transportation",
                "entity_value": "public transportation", "confidence_score": 90}
        ]

        for entity_data in entities_data:
            entity = Entity(**entity_data)
            session.add(entity)

        await session.commit()
        print(f"Created {len(entities_data)} entities")

        print("\nDatabase seeded successfully!")
        print(
            f"Created: {len(users)} users, {len(conversations)} conversations, {len(messages)} messages, {len(entities_data)} entities")


def main():
    """Main function to run the seeding script"""
    print("Starting database seeding...")
    try:
        asyncio.run(seed_data())
        print("Seeding completed successfully!")
    except Exception as e:
        print(f"Seeding failed: {e}")


if __name__ == "__main__":
    main()
