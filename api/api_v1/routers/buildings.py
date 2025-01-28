from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud.buildings import get_buildings_in_radius, \
    get_buildings_in_square
from core.models import db_helper
from core.schemas.building import BuildingResponse
from utils.get_api_key import get_api_key

router = APIRouter(
    prefix='/buildings',
    tags=['Buildings']
)


@router.get('/buildings/round-search', response_model=List[BuildingResponse],
            name='Поиск зданий в некотором радиусе (задаваемом в метрах) относительно заданной точки')
async def search_buildings_in_radius(
        longitude: float,
        latitude: float,
        radius: float,
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(db_helper.session_getter),

):
    buildings = get_buildings_in_radius(session=session, longitude=longitude, latitude=latitude, radius=radius)
    return await buildings


@router.post('/buildings/square-search', response_model=List[BuildingResponse],
             name='Поиск зданий в квадратной области, которая задается двумя противолежащими точками')
async def search_buildings_in_radius(
        # [[30.314560, 59.939832], [37.540000, 55.749200]], [[37.537932, 55.749792], [37.617734, 55.751999]]
        points: list[list[float]],
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(db_helper.session_getter),

):
    buildings = get_buildings_in_square(session=session, points=points)
    return await buildings
