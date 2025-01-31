import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


async def test_get_buildings_from_point_by_radius_200(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/buildings/buildings/round-search?longitude=27&latitude=47&radius=1000000",
        headers={'access_token': 'static_api_key'}
    )
    orgs = response.json()

    assert response.status_code == 200
    assert len(orgs) == 1
    assert orgs[0]['id'] == 3
    assert orgs[0]['address'] == 'Test_Address_3'
    assert orgs[0]['coords'] == 'POINT (30.593217 51.857392)'


async def test_get_buildings_from_point_by_radius_403(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/buildings/buildings/round-search?longitude=27&latitude=47&radius=1000000"
    )

    assert response.status_code == 403


async def test_get_buildings_from_point_by_radius_404(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/buildings/buildings/round-search?longitude=27&latitude=47&radius=1",
        headers={'access_token': 'static_api_key'}
    )
    orgs = response.json()

    assert response.status_code == 404
    assert orgs['detail'] == 'There are no buildings in this area'

async def test_get_buildings_from_point_by_radius_422(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/buildings/buildings/round-search?longitude=asd&latitude=47&radius=1000000",
        headers={'access_token': 'static_api_key'}
    )
    orgs = response.json()

    assert response.status_code == 422
    assert orgs['detail'][0]['msg'] == 'Input should be a valid number, unable to parse string as a number'


async def test_get_buildings_by_square(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "api/api_v1/buildings/buildings/square-search",
        json=[[31,40], [40,70]],
        headers={'access_token': 'static_api_key'}
    )
    orgs = response.json()

    assert response.status_code == 200
    assert len(orgs) == 2
    assert orgs[0] == {'address': 'Test_Address_1', 'coords': 'POINT (32.847193 53.102847)', 'id': 1}
    assert orgs[1] == {'address': 'Test_Address_2', 'coords': 'POINT (34.291074 50.628491)', 'id': 2}

async def test_get_buildings_by_square_403(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "api/api_v1/buildings/buildings/square-search",
        json=[[31, 40], [40, 70]]
    )
    assert response.status_code == 403


async def test_get_buildings_by_square_404(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "api/api_v1/buildings/buildings/square-search",
        json=[[50, 70], [70, 90]],
        headers={'access_token': 'static_api_key'}
    )
    orgs = response.json()

    assert response.status_code == 404
    assert orgs['detail'] == 'There are no buildings in this area'
