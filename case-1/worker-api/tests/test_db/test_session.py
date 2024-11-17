import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_get_db(db_session: AsyncSession):
    assert isinstance(db_session, AsyncSession)
    result = await db_session.execute("SELECT 1")
    assert result.scalar() == 1
