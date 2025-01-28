from sqlalchemy import ForeignKey, Table, Column

from core.models import Base


organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id")),
    Column("activity_id", ForeignKey("activities.id")),
)
