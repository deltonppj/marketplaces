from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Session


async def get_session() -> Generator:
    """
    Get a new session from the database.
    """
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()
