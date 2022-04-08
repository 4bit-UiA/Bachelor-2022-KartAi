from common import config
import datetime
from src.eksperiment_johannes.similarity_analysis import measure_iou_of_observations
import eksperiment_biou as biou
from shapely.geometry import Polygon
from itertools import chain


class Observation:
    def __init__(self, observation_id, dataset, date, polygon_geojson):
        self.ID = observation_id
        self.dataset = dataset
        self.date = date
        self.shape = Shape(polygon_geojson)


class Shape:
    def __init__(self, polygon_geojson):
        self.polygon = Polygon(list(chain(*polygon_geojson['coordinates'])))
        self.BIOU = None
        self.congruent = None
        self.area = None  # set with shapely math

    def update_comparison(self, new_observation: Observation):
        #self.IOU = measure_iou_of_observations(self.polygon, new_observation.shape.polygon)
        self.BIOU = biou.measure_biou(self.polygon, new_observation.shape.polygon)
        self.congruent = True if self.BIOU > float(config['iouthreshold']) else False
        return self.congruent


if __name__ == "__main__":    
    test = Observation(1, "flyfoto", datetime.datetime.now(), {"x":69, "y":420})

    print(vars(test))
    print(vars(test.shape))


def find_reliability(new_observation, base_reliability):
    #list_of_observations = SELECT * FROM observations WHERE id = new_observation.ID
    valid_observations = list_of_observations[find_first_congruent(list_of_observations):]
    next_multiplier = 0.5
    incongruent_observations = 0
    current_reliability = base_reliability
    for obs in valid_observations:
        obs.shape.update_comparison(new_observation)
        if obs.shape.congruent:
            current_reliability = current_reliability + current_reliability * next_multiplier
            next_multiplier = next_multiplier / 2
        else:
            incongruent_observations += 1

    reliability = current_reliability - current_reliability / incongruent_observations



def find_first_congruent(list_of_observations):
    for i in range(len(list_of_observations)):
        if list_of_observations[i].congruent:
            return i
