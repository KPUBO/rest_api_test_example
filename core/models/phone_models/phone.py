from sqlalchemy import UniqueConstraint, String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models import Base
from core.models.orgs_models.org import Organization


class Phone(Base):
    __tablename__ = 'phones'

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    number: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    organizations: Mapped[Organization] = relationship(back_populates="phones")

    __table_args__ = (UniqueConstraint('organization_id', 'number'),)
