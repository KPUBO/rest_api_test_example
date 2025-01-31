from geoalchemy2 import WKBElement
from shapely.wkt import loads
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.models import Building


def str_to_wkb(string):
    wkb_data = loads(string).wkb
    coords = WKBElement(wkb_data, srid=4326)
    return coords


buildings = [
    Building(id=1,
             address='Test_Address_1',
             coords=str_to_wkb('POINT(32.847193 53.102847)')),
    Building(id=2,
             address='Test_Address_2',
             coords=str_to_wkb('POINT(34.291074 50.628491)')),
    Building(id=3,
             address='Test_Address_3',
             coords=str_to_wkb('POINT(30.593217 51.857392)'))
]


async def buildings_insert(session: AsyncSession):
    session.add_all(buildings)
    await session.commit()
