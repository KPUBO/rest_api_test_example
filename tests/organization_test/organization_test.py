import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

pytestmark = pytest.mark.asyncio


async def test_get_orgs_by_buildings_id_200_building_1(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/organizations/buildings/1",
        headers={'access_token': 'static_api_key'}
    )
    orgs = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(orgs) == 2
    assert orgs[0]['id'] == 1
    assert orgs[1]['id'] == 2
    assert orgs[0]['buildings']['id'] == 1
    assert orgs[1]['buildings']['id'] == 1
    assert orgs[0]['buildings']['coords'] == 'POINT (32.847193 53.102847)'


async def test_get_orgs_by_buildings_id_200_building_2(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/organizations/buildings/2",
        headers={'access_token': 'static_api_key'}
    )
    orgs = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(orgs) == 2
    assert orgs[0]['id'] == 3
    assert orgs[1]['id'] == 4
    assert orgs[0]['buildings']['id'] == 2
    assert orgs[1]['buildings']['id'] == 2
    assert orgs[0]['buildings']['coords'] == 'POINT (34.291074 50.628491)'


async def test_get_orgs_by_buildings_id_403(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/organizations/buildings/1"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_get_orgs_by_buildings_id_404(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/organizations/buildings/1000",
        headers={'access_token': 'static_api_key'}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_orgs_by_activity_id_200_activity_1(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/organizations/activities/1",
        headers={'access_token': 'static_api_key'}
    )
    orgs = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(orgs) == 1
    assert orgs[0]['id'] == 1
    assert orgs[0]['activities'][0]['id'] == 1


async def test_get_orgs_by_activity_id_200_activity_5(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/organizations/activities/5",
        headers={'access_token': 'static_api_key'}
    )
    orgs = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(orgs) == 2
    assert orgs[0]['id'] == 1
    assert orgs[1]['id'] == 5
    assert orgs[0]['activities'][1]['id'] == 5
    assert orgs[1]['activities'][0]['id'] == 5


async def test_get_orgs_by_activity_id_403(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/organizations/activities/1"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_get_orgs_by_activity_id_404(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/organizations/activities/1000",
        headers={'access_token': 'static_api_key'}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_org_by_id_200(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/api_v1/organizations/{org_id}?organization_id=1",
        headers={'access_token': 'static_api_key'}
    )
    org = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert org["id"] == 1
    assert org["name"] == 'Test_OrgName_1'
    assert org['building_id'] == 1
    assert org['buildings']['coords'] == 'POINT (32.847193 53.102847)'
    assert len(org['activities']) == 2
    assert org['activities'][0]['id'] == 1
    assert org['activities'][1]['id'] == 5


async def test_get_org_by_id_403(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/api_v1/organizations/{org_id}?organization_id=1"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_get_org_by_id_404(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/api_v1/organizations/{org_id}?organization_id=1000",
        headers={'access_token': 'static_api_key'}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_orgs_by_activity_tree_finder_200_activity_1(async_client: AsyncClient,
                                                               async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/api_v1/organizations/tree_find/1",
        headers={'access_token': 'static_api_key'}
    )
    org = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(org) == 4
    assert [org[0]['id'], org[1]['id'], org[2]['id'], org[3]['id']] == [1, 2, 3, 4]
    assert (org[0]['name'],
            org[1]['name'],
            org[2]['name'],
            org[3]['name']) == ('Test_OrgName_1', 'Test_OrgName_2', 'Test_OrgName_3', 'Test_OrgName_4')
    assert org[0]['activities'][0] == {'id': 1, 'level': 1, 'name': 'Test_Activity_1', 'parent_id': None}
    assert org[1]['activities'] == [{'id': 2, 'level': 2, 'name': 'Test_Activity_2', 'parent_id': 1}]
    assert org[2]['activities'] == [{'id': 3, 'level': 3, 'name': 'Test_Activity_3', 'parent_id': 2}]
    assert org[3]['activities'] == [{'id': 4, 'level': 3, 'name': 'Test_Activity_4', 'parent_id': 2}]


async def test_get_orgs_by_activity_tree_finder_200_activity_2(async_client: AsyncClient,
                                                               async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/api_v1/organizations/tree_find/2",
        headers={'access_token': 'static_api_key'}
    )
    org = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(org) == 3
    assert [org[0]['id'], org[1]['id'], org[2]['id']] == [2, 3, 4]
    assert [org[0]['name'],
            org[1]['name'],
            org[2]['name']] == ['Test_OrgName_2', 'Test_OrgName_3', 'Test_OrgName_4']
    assert org[0]['activities'] == [{'id': 2, 'level': 2, 'name': 'Test_Activity_2', 'parent_id': 1}]
    assert org[1]['activities'] == [{'id': 3, 'level': 3, 'name': 'Test_Activity_3', 'parent_id': 2}]
    assert org[2]['activities'] == [{'id': 4, 'level': 3, 'name': 'Test_Activity_4', 'parent_id': 2}]


async def test_get_orgs_by_activity_tree_finder_403(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/api_v1/organizations/tree_find/1"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_get_orgs_by_activity_tree_finder_404(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/api_v1/organizations/tree_find/1000",
        headers={'access_token': 'static_api_key'}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_org_by_name_200_org_1(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/organizations/find-organization-by-name/{org_name}?organization_name=Test_OrgName_1",
        headers={'access_token': 'static_api_key'}
    )
    org = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert org["id"] == 1
    assert org["name"] == 'Test_OrgName_1'


async def test_get_org_by_name_200_org_4(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/organizations/find-organization-by-name/{org_name}?organization_name=Test_OrgName_4",
        headers={'access_token': 'static_api_key'}
    )
    org = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert org["id"] == 4
    assert org["name"] == 'Test_OrgName_4'


async def test_get_org_by_name_403(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/organizations/find-organization-by-name/{org_name}?organization_name=Test_OrgName_1"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_get_org_by_name_404(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/api_v1/organizations/find-organization-by-name/{org_name}?organization_name=Random_Name",
        headers={'access_token': 'static_api_key'}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
