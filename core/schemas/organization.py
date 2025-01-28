from typing import List

from pydantic import BaseModel

from core.schemas.activity import ActivityRead
from core.schemas.building import BuildingResponse
from core.schemas.phone import PhoneRead


class OrganizationBase(BaseModel):
    name: str
    building_id: int


class OrganizationCreate(OrganizationBase):
    activity_id: int


class OrganizationRead(OrganizationBase):
    id: int
    phones: list[PhoneRead]
    buildings: BuildingResponse
    activities: List[ActivityRead]
