from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.models.m2m_models.org_activity import organization_activity


async def query_execution(session: AsyncSession, org_id: int, activity_id: int):
    query = organization_activity.insert().values(organization_id=org_id, activity_id=activity_id)
    await session.execute(query)


org_activity_connection = [
    {
        'organization_id': 1,
        'activity_id': 1
    },
    {
        'organization_id': 1,
        'activity_id': 5
    },
    {
        'organization_id': 2,
        'activity_id': 2
    },
    {
        'organization_id': 3,
        'activity_id': 3
    },
    {
        'organization_id': 4,
        'activity_id': 4
    },
    {
        'organization_id': 5,
        'activity_id': 5
    },

]


async def org_activity_insert(session: AsyncSession):
    for conn in org_activity_connection:
        await query_execution(session, conn['organization_id'], conn['activity_id'])
    await session.commit()
