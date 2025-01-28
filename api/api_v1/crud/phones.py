from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Phone
from core.schemas.phone import PhoneCreate


async def get_all_phones(session: AsyncSession) -> Sequence[Phone]:
    stmt = select(Phone).order_by(Phone.id)
    res = await session.scalars(stmt)
    return res.all()


async def create_phone(session: AsyncSession, phone: PhoneCreate) -> Phone:
    phone = Phone(**phone.model_dump())
    session.add(phone)
    await session.commit()
    await session.refresh(phone)
    return phone
