from typing import Optional

from pydantic import BaseModel


class BuildingBase(BaseModel):
    address: str
    coords: str


class BuildingCreate(BuildingBase):
    pass


class BuildingResponse(BuildingBase):
    id: int
    coords: Optional[str]
