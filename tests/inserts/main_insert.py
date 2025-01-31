from sqlalchemy.ext.asyncio import AsyncSession

from tests.inserts.activities_insert import activities_insert
from tests.inserts.buildings_insert import buildings_insert
from tests.inserts.org_activity_insert import org_activity_insert
from tests.inserts.organizations_insert import organizations_insert
from tests.inserts.phones_insert import phones_insert


async def insert_test_datas(session: AsyncSession):
    await buildings_insert(session)
    await activities_insert(session)
    await organizations_insert(session)
    await org_activity_insert(session)
    await phones_insert(session)
    await session.commit()
