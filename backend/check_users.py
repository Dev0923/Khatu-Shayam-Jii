import asyncio
from sqlalchemy import select
from database import AsyncSessionLocal
from models.sql_models import User

async def run():
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User))
        print([(u.email, u.is_admin) for u in res.scalars().all()])

if __name__ == "__main__":
    asyncio.run(run())
