from geoalchemy2 import Geometry, WKTElement, WKBElement
from sqlalchemy import String, Column
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models import Base


class Building(Base):
    address: Mapped[str] = mapped_column(String, unique=True)
    coords: Mapped[WKBElement] = Column(Geometry(geometry_type="POINT", srid=4326, spatial_index=False))

    @property
    def coords_as_wkt(self):
        from geoalchemy2.shape import to_shape
        shapely_geom = to_shape(self.coords)
        return shapely_geom.wkt

    organizations: Mapped[list["Organization"]] = relationship(back_populates="buildings")
