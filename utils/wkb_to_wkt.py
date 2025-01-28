from geoalchemy2 import WKTElement, WKBElement

from core.models import Building
from geoalchemy2.shape import to_shape


def coords_as_wkt(building: Building):
    if type(building.coords) == WKTElement or type(building.coords) == WKBElement:
        shapely_geom = to_shape(building.coords)
        building.coords = shapely_geom.wkt
    else:
        pass

