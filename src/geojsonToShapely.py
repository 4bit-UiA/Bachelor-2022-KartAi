from shapely.geometry import Polygon
from itertools import chain
import json


def geojson_to_shape(geojsonfile):
    jso = json.load(open(geojsonfile, "r"))
    poly = Polygon(list(chain(*jso['features'][0]['geometry']['coordinates'])))
    return poly

