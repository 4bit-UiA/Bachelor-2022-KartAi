import datetime
#from similarity_analysis import measure_iou_of_observations

class Observation:
    def __init__(self, observation_id, dataset, date, polygon):
        self.ID = observation_id
        self.dataset = dataset
        self.date = date
        self.shape = Shape(polygon)


class Shape:
    def __init__(self, polygon):
        self.polygon = polygon
        self.IOU = None
        self.congruent = None
        self.area = None  # set with shapely math

    def update(self, new_observation):
        self.IOU = measure_iou_of_observations(self.polygon, new_observation)
        self.congruent = True if self.IOU > 95 else False


if __name__ == "__main__":
    
    test = Observation(1, "flyfoto", datetime.datetime.now(), {"x":69, "y":420})

    print(vars(test))
    print(vars(test.shape))


def find_reliability(base_reliability):
    base_reliability = base_reliability
    valid_observations = list_of_observations[find_first_congruent():]


def find_first_congruent():
    for i in range(len(list_of_observations)):
        if list_of_observations[i].congruent:
            return i
