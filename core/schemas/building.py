from typing import Optional

from pydantic import BaseModel


class BuildingBase(BaseModel):
    address: str
    coords: str


class BuildingCreate(BuildingBase):
    pass


class BuildingResponse(BaseModel):
    id: int
    coords: Optional[str]
