from typing import Sequence

from fastapi import HTTPException
from geoalchemy2 import WKTElement
from geoalchemy2.functions import ST_DWithin, ST_Transform, ST_MakeEnvelope, ST_Within
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.building_models.building import Building
from core.schemas.building import BuildingCreate
from utils.wkb_to_wkt import coords_as_wkt


async def get_all_buildings(session: AsyncSession) -> Sequence[Building]:
    stmt = select(Building).order_by(Building.id)
    res = await session.scalars(stmt)
    buildings = res.all()
    for building in buildings:
        coords_as_wkt(building)
    if buildings is None:
        raise HTTPException(status_code=404, detail="Buildings not found")
    return buildings


async def create_building(session: AsyncSession, building: BuildingCreate) -> Building:
    building.coords = WKTElement(building.coords, srid=4326)
    building = Building(**building.model_dump())
    session.add(building)
    await session.commit()
    await session.refresh(building)
    coords_as_wkt(building)
    return building


async def get_buildings_in_radius(session: AsyncSession, latitude: float, longitude: float, radius: float) -> Sequence[
    Building]:
    point = WKTElement(f"POINT({longitude} {latitude})", srid=4326)

    stmt = (
        select(Building)
        .filter(ST_DWithin(ST_Transform(Building.coords, 3857), ST_Transform(point, 3857), radius))
    )

    result = await session.execute(stmt)
    buildings = result.scalars().all()
    if buildings is None or len(buildings) == 0:
        raise HTTPException(status_code=404, detail="There are no buildings in this area")
    for building in buildings:
        coords_as_wkt(building)

    return buildings


async def get_buildings_in_square(session: AsyncSession, points: list[list[float]]) -> Sequence[Building]:
    points = list(points)
    longitudes = [points[0][0], points[1][0]]
    latitudes = [points[0][1], points[1][1]]

    envelope = ST_MakeEnvelope(min(longitudes), min(latitudes), max(longitudes), max(latitudes), 4326)

    query = select(Building).where(
        ST_Within(Building.coords, envelope)
    )

    result = await session.execute(query)
    buildings = result.scalars().all()
    if buildings is None or len(buildings) == 0:
        raise HTTPException(status_code=404, detail="There are no buildings in this area")
    for building in buildings:
        coords_as_wkt(building)

    return buildings