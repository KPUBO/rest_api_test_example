from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.models import Organization

organizations = [
    Organization(id=1,
                 name='Test_OrgName_1',
                 building_id=1),
    Organization(id=2,
                 name='Test_OrgName_2',
                 building_id=1),
    Organization(id=3,
                 name='Test_OrgName_3',
                 building_id=2),
    Organization(id=4,
                 name='Test_OrgName_4',
                 building_id=2),
    Organization(id=5,
                 name='Test_OrgName_5',
                 building_id=3),
]


async def organizations_insert(session: AsyncSession):
    session.add_all(organizations)
    await session.commit()
