from typing import Optional

from pydantic import BaseModel


class ActivityBase(BaseModel):
    name: str
    level: Optional[int]
    parent_id: Optional[int]


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int