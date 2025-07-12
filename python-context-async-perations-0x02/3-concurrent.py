import asyncio
import aiosqlite

DB_NAME = "example.db"

async def async_fetch_users():
    """
    Asynchronously fetch all users from the database.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        print("All users:")
        for row in rows:
            print(row)

async def async_fetch_older_users():
    """
    Asynchronously fetch users older than 40.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        rows = await cursor.fetchall()
        await cursor.close()
        print("Users older than 40:")
        for row in rows:
            print(row)

async def fetch_concurrently():
    """
    Run both fetch functions concurrently using asyncio.gather().
    """
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
