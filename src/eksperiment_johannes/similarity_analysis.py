import json
from geojson import FeatureCollection
from shapely.geometry import Polygon, Point
from area import area
from turfpy.transformation import intersect
from src.eksperiment_johannes.helper_functions import union


class Observation:
    def __init__(self, date, dataset, geo_type, coordinates, obs_area, geojson):
        self.date = date
        self.dataset = dataset
        self.geo_type = geo_type
        self.coordinates = coordinates
        self.area = obs_area
        self.geojson = geojson

    def __repr__(self):
        return '{' + self.date + ', ' + self.dataset + ', ' + str(self.coordinates) + "}"


# Returns a list of Observation objects based on the dictionary of geojson data input.
def load_observations_from_file(jsonfile) -> list:
    loaded_data = json.load(open(jsonfile, "r"))
    list_of_observations = []
    for key in loaded_data['features']:
        properties = key['properties']
        geometry = key['geometry']
        coordinates = geometry['coordinates'][0] if (len(geometry['coordinates']) == 1) else geometry['coordinates']
        geojson_area = round(area(geometry), 4)
        observation = Observation(
            properties['date'],
            properties['dataset'],
            geometry['type'],
            coordinates,
            geojson_area,
            key)

        list_of_observations.append(observation)
    return list_of_observations


def measure_iou_of_observations(observation_1: Observation, observation_2: Observation) -> float:
    coordinates_1 = observation_1.geojson
    coordinates_2 = observation_2.geojson
    intersection = intersect([coordinates_1, coordinates_2])
    union_ = union(FeatureCollection([coordinates_1, coordinates_2], properties={"combine": "yes"}))
    area_of_intersection = area(intersection['geometry'])
    area_of_union = area(union_['geometry'])
    return area_of_intersection / area_of_union


def difference_in_area(area1: float, area2: float) -> float:
    return round(area1 - area2, 4)


if __name__ == "__main__":
    data = load_observations_from_file("../../resources/observasjoner_2021.json") \
           + load_observations_from_file("../../resources/observasjoner_2020.json") \
           + load_observations_from_file("../../resources/observasjoner_2022.json")

    # Sorterer alle observasjon objekter etter dato
    data.sort(key=lambda obs: obs.date)

    for i in range(len(data)):
        curr_observation = data[i]
        print(
            curr_observation.date + " - " + curr_observation.dataset + " - " + curr_observation.geo_type + " - " + str(
                curr_observation.area) + "m²")
        if i == 0:  # Første observasjon ignoreres.
            print("|     First Observation")
        else:  # Hver observasjon sammenlignes med tidligere observasjoner. Både flater og punkt.
            for j in range(i, 0, -1):
                last_observation = data[j - 1]
                if len(curr_observation.coordinates) > 2:
                    if len(last_observation.coordinates) > 2:
                        difference_in_area_ = difference_in_area(curr_observation.area, last_observation.area)
                        iou_of_observations = measure_iou_of_observations(curr_observation, last_observation)
                        print(
                            "|    Difference in area: " + last_observation.date + " - " + last_observation.dataset
                            + ": " + str(difference_in_area_) + "m²"
                        )
                        print(
                            "|    IOU of current observation and " + last_observation.date + " - "
                            + last_observation.dataset + ": " + str(iou_of_observations))
                        print("____________________________________________________________________")
                    else:
                        point = Point(last_observation.coordinates)
                        polygon = Polygon(curr_observation.coordinates)
                        print(
                            "|    " + last_observation.date + " - " + last_observation.dataset + " exists in between this observation's coordinates: " + str(
                                polygon.contains(point)))
                elif len(curr_observation.coordinates) == 2:
                    point1 = Point(curr_observation.coordinates)
                    point_or_polygon = Polygon(last_observation.coordinates) if len(last_observation.coordinates) > 2 \
                        else Point(last_observation.coordinates)
                    print(
                        "|    Point is present in  - " + last_observation.date + " - " + last_observation.dataset + ": "
                        + str(point_or_polygon.contains(point1))
                        + "\n____________________________________________________________________"
                    )

        print("\n\n")
