from __future__ import annotations

from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models import Base
from core.models.m2m_models.org_activity import organization_activity


class Organization(Base):
    __tablename__ = 'organizations'
    name: Mapped[str] = mapped_column(String, unique=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False)

    buildings: Mapped["Building"] = relationship(back_populates="organizations")
    phones: Mapped[list["Phone"]] = relationship(back_populates="organizations")

    activities: Mapped[List["Activity"]] = relationship(
        secondary=organization_activity, back_populates="organizations"
    )
