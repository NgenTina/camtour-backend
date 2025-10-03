import asyncio
from asyncpg import connect

async def test_connection():
    conn = await connect("postgresql://postgres:postgres@localhost:5432/postgres")
    print("Connection successful!")
    await conn.close()

asyncio.run(test_connection())