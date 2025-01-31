from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.models import Activity

activities = [
    Activity(id=1,
             name='Test_Activity_1',
             level=1,
             parent_id=None),
    Activity(id=2,
             name='Test_Activity_2',
             level=2,
             parent_id=1),
    Activity(id=3,
             name='Test_Activity_3',
             level=3,
             parent_id=2),
    Activity(id=4,
             name='Test_Activity_4',
             level=3,
             parent_id=2),
    Activity(id=5,
             name='Test_Activity_5',
             level=1,
             parent_id=None),

]


async def activities_insert(session: AsyncSession):
    session.add_all(activities)
    await session.commit()
