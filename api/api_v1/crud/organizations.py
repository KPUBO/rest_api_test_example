from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.api_v1.crud.activities import test_tree_finder
from core.models import Activity
from core.models.m2m_models.org_activity import organization_activity
from core.models.orgs_models.org import Organization
from core.schemas.organization import OrganizationCreate
from utils.wkb_to_wkt import coords_as_wkt


async def get_all_organizations(session: AsyncSession) -> Sequence[Organization]:
    stmt = select(Organization).options(
        joinedload(Organization.phones),
        joinedload(Organization.activities),
        joinedload(Organization.buildings)
    ).order_by(Organization.id)

    result = await session.execute(stmt)

    organizations = result.unique().scalars().all()
    if organizations is None:
        raise HTTPException(status_code=404, detail="Buildings not found")
    for org in organizations:
        coords_as_wkt(org.buildings)

    return organizations


async def get_organization_by_id(session, organization_id):
    org_1 = await session.execute(select(Organization).filter(Organization.id == 1))
    org_1 = org_1.scalars().first()
    activity_1 = await session.execute(select(organization_activity).filter(Organization.id == 1))
    activity_1 = activity_1.scalars().first()
    result = await session.execute(
        select(Organization)
        .options(
            joinedload(Organization.phones),
            joinedload(Organization.activities),
            joinedload(Organization.buildings)

        )
        .filter(Organization.id == organization_id)
    )
    organization = result.scalars().first()
    if organization is None:
        raise HTTPException(status_code=404, detail="Buildings not found")
    coords_as_wkt(organization.buildings)
    return organization


async def create_organization(session: AsyncSession, organization: OrganizationCreate, activity_id) -> Organization:
    organization = Organization(**organization.model_dump())
    result = await session.execute(
        select(Activity).where(Activity.id == activity_id)
    )
    activity = result.scalars().first()
    organization.activities.append(activity)
    session.add(organization)
    await session.commit()
    await session.refresh(organization)
    return organization


async def find_organizations_by_building_id(session: AsyncSession, building_id: int) -> Sequence[Organization]:
    stmt = select(Organization).where(Organization.building_id == building_id)
    result = await session.execute(stmt)
    organizations = result.scalars().all()
    if organizations is None or len(organizations) == 0:
        raise HTTPException(status_code=404, detail="Organizations not found")
    result = []
    for org in organizations:
        res = await get_organization_by_id(session, org.id)
        result.append(res)
    return organizations


async def find_organizations_by_activity_id(session: AsyncSession, activity_id: int) -> Sequence[Organization]:
    stmt = (
        select(Organization)
        .join(Organization.activities)
        .filter(Activity.id == activity_id)
        .options(joinedload(Organization.activities))
    )

    result = await session.execute(stmt)
    organizations = result.unique().scalars().all()
    if organizations is None or len(organizations) == 0:
        raise HTTPException(status_code=404, detail="Buildings not found")
    result = []
    for org in organizations:
        res = await get_organization_by_id(session, org.id)
        result.append(res)
    return organizations


async def find_organization_by_name(session: AsyncSession, name: str) -> Organization:
    result = await session.execute(
        select(Organization)
        .options(
            joinedload(Organization.phones),
            joinedload(Organization.activities),
            joinedload(Organization.buildings)

        )
        .filter(Organization.name == name)
    )
    organization = result.scalars().first()
    if organization is None:
        raise HTTPException(status_code=404, detail="Buildings not found")
    coords_as_wkt(organization.buildings)
    return organization


async def organizations_tree_finder(session: AsyncSession, activity_id):
    result = []
    activities = await test_tree_finder(session, activity_id)
    for activity_number in activities:
        try:
            org = await find_organizations_by_activity_id(session, activity_number)
            if org:
                result.append(org[0])
        except HTTPException:
            pass
    if result is None or len(result) == 0:
        raise HTTPException(status_code=404, detail="Organizations not found")
    return result
