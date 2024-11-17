import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db


@pytest.mark.asyncio
async def test_get_db(db_session: AsyncSession):
    async for session in get_db():
        assert isinstance(session, AsyncSession)
        result = await session.execute("SELECT 1")
        assert result.scalar() == 1
