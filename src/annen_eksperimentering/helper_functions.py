from typing import List, Union

from geojson import Feature, FeatureCollection

from shapely.geometry import mapping, shape
from shapely.ops import unary_union

from turfpy.helper import get_geom

# oppdatert union(). union() fra shapely biblioteket er deprecated.
def union(
        features: Union[List[Feature], FeatureCollection]
) -> Union[Feature, FeatureCollection]:
    shapes = []
    properties_list = []
    if isinstance(features, list):
        for f in features:
            if f.type != "Feature":
                raise Exception("Not a valid feature")
            geom = get_geom(f)
            s = shape(geom)
            shapes.append(s)

            if "properties" in f.keys():
                properties_list.append(f["properties"])
    else:
        if "features" not in features.keys():
            raise Exception("Invalid FeatureCollection")
        if "properties" in features.keys():
            properties_list.append(features["properties"])

        for f in features["features"]:
            geom = get_geom(f)
            s = shape(geom)
            shapes.append(s)

            if "properties" in f.keys():
                properties_list.append(f["properties"])

    result = unary_union(shapes)
    result = mapping(result)
    properties = merge_dict(properties_list)

    if result["type"] == "GeometryCollection":
        features = []
        for geom in result["geometries"]:
            features.append(Feature(geometry=geom))
        return FeatureCollection(features, properties=properties)

    return Feature(geometry=result, properties=properties)


def merge_dict(dicts: list):
    super_dict: dict = {}
    for d in dicts:
        for k, v in d.items():
            if k not in super_dict.keys():
                super_dict[k] = v
            else:
                if isinstance(super_dict[k], list):
                    if v not in super_dict[k]:
                        super_dict[k].append(v)
                else:
                    if super_dict[k] != v:
                        super_dict[k] = [super_dict[k], v]
    return super_dict
