from pydantic import BaseModel


class PhoneBase(BaseModel):
    organization_id: int
    number: str


class PhoneCreate(PhoneBase):
    pass


class PhoneRead(PhoneBase):
    id: int
