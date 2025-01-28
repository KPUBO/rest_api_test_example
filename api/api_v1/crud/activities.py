from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Activity
from core.schemas.activity import ActivityCreate


async def get_all_activities(session: AsyncSession) -> Sequence[Activity]:
    stmt = select(Activity).order_by(Activity.id)
    res = await session.scalars(stmt)
    return res.all()


async def get_activity_by_id(session: AsyncSession, activity_id: int) -> Activity:
    stmt = select(Activity).where(Activity.id == activity_id)
    res = await session.execute(stmt)
    activity = res.scalars().first()
    return activity


async def create_activity(session: AsyncSession, activity: ActivityCreate) -> Activity:
    activity = Activity(**activity.model_dump())
    session.add(activity)
    await session.commit()
    await session.refresh(activity)
    return activity


async def test_tree_finder(session: AsyncSession, activity_id: int):
    activity_hierarchy = select(
        Activity.id,
        Activity.parent_id,
        Activity.name,
        Activity.level
    ).where(Activity.id == activity_id).cte(recursive=True)

    recursive_query = select(
        Activity.id,
        Activity.parent_id,
        Activity.name,
        Activity.level
    ).join(
        activity_hierarchy,
        Activity.parent_id == activity_hierarchy.c.id
    )

    activity_hierarchy = activity_hierarchy.union_all(recursive_query)

    final_query = select(activity_hierarchy)

    result = await session.execute(final_query)

    return result.scalars().all()
