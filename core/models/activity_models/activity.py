from typing import List

from sqlalchemy import String, Integer, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models import Base
from core.models.m2m_models.org_activity import organization_activity
from core.models.orgs_models.org import Organization

MAX_LEVEL = 3


class Activity(Base):

    __tablename__ = 'activities'

    parent_id: Mapped[id] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String)
    level: Mapped[int] = mapped_column(Integer)

    organizations: Mapped[List["Organization"]] = relationship(
        secondary=organization_activity, back_populates="activities"
    )

    __table_args__ = (
        CheckConstraint(f'level <= {MAX_LEVEL}', name='check_level'),
    )
