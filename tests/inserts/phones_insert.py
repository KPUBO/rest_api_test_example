from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.models import Phone

phones = [
    Phone(id=1,
          number='+7 (912) 345-67-89',
          organization_id=1),
    Phone(id=2,
          number='+7 (926) 678-90-12',
          organization_id=1),
    Phone(id=3,
          number='+7 (931) 234-56-78',
          organization_id=2),
    Phone(id=4,
          number='+7 (950) 789-12-34',
          organization_id=2),
    Phone(id=5,
          number='+7 (977) 456-78-90',
          organization_id=3),
    Phone(id=6,
          number='+7 (988) 567-89-01',
          organization_id=4),
    Phone(id=7,
          number='+7 (999) 123-45-67',
          organization_id=4),
    Phone(id=8,
          number='+7 (905) 876-54-32',
          organization_id=5)
]


async def phones_insert(session: AsyncSession):
    session.add_all(phones)
    await session.commit()
