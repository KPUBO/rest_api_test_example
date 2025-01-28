from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud.organizations import get_organization_by_id, \
    find_organizations_by_building_id, find_organizations_by_activity_id, find_organization_by_name, \
    organizations_tree_finder
from core.models import db_helper
from core.schemas.organization import OrganizationRead
from utils.get_api_key import get_api_key

router = APIRouter(
    prefix='/organizations',
    tags=['Organizations']
)


@router.get('/{org_id}', response_model=OrganizationRead,
            name='Получение информации об организации по ее идентификатору')
async def get_organization(
        organization_id: int,
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(db_helper.session_getter),

):
    organizations = await get_organization_by_id(session=session, organization_id=organization_id)
    return organizations


@router.get('/find-organization-by-name/{org_name}', response_model=OrganizationRead,
            name='Получение информации об организации по ее названию')
async def get_organization(
        organization_name: str,
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(db_helper.session_getter),

):
    organization = await find_organization_by_name(session=session, name=organization_name)
    return organization


@router.get('/buildings/{building_id}', response_model=List[OrganizationRead],
            name='Получение списка организаций, находящихся в одном здании (здание задается идентификатором)')
async def get_organizations_by_building_id(
        building_id: int,
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(db_helper.session_getter),

):
    organizations = await find_organizations_by_building_id(session=session, building_id=building_id)
    return organizations


@router.get('/activities/{activity_id}', response_model=List[OrganizationRead],
            name='Получение списка организаций, занимающихся видом деятельности, задаваемым идентификатором')
async def get_organizations_by_activity_id(
        activity_id: int,
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(db_helper.session_getter),

):
    organizations = await find_organizations_by_activity_id(session=session, activity_id=activity_id)
    return organizations


@router.get('/tree_find/{activity_id}', response_model=List[OrganizationRead],
            name='Древовидный поиск организаций, занимающихся видом деятельности, задаваемым идентификатором')
async def get_organizations_by_activity_id_tree_finder(
        activity_id: int,
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    organizations = await organizations_tree_finder(session=session, activity_id=activity_id)
    return organizations
