from common import config
import datetime
import eksperiment_biou as biou
from shapely.geometry import Polygon
from itertools import chain
from src.DB.db_connection import connect_to_db
import json


class Observation:
    def __init__(self, observation_id, dataset, date, polygon_geojson, geoid):
        self.ID = observation_id
        self.dataset = dataset
        self.date = date
        self.shape = Shape(json.loads(polygon_geojson))
        self.geoid = geoid


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


def find_reliability(new_observation: Observation):
    # Hente observasjoner fra databasen.
    list_of_observations = get_observations_from_db(new_observation.geoid)

    for obs in list_of_observations:
        obs.shape.update_comparison(new_observation)

    # Liste over observasjoner fra den første som er enig. (Lista er sortert kronologisk)
    valid_observations = list_of_observations[find_first_congruent(list_of_observations):]

    # 
    next_multiplier = 0.5
    incongruent_observations = 0
    total_valid_observations = 0

    #setter utgangspunktet for pålitelighet basert på dataset. forhåndsdefinert i config.
    current_reliability = float(config['basereliability' + new_observation.dataset ])
    
    for obs in list_of_observations:
        if obs.ID != new_observation.ID:
            #print(obs.ID, obs.shape.BIOU, obs.shape.congruent)
            print(obs.shape.BIOU)
            # Hvis observasjonen er enig i endringen, øk påliteligheten i samsvar med "next multiplier", og halverer multiplier til neste gang.
            if obs.shape.congruent:
                current_reliability = current_reliability + (current_reliability * next_multiplier)
                next_multiplier = next_multiplier / 2
            else:
                incongruent_observations += 1
            total_valid_observations += 1

    # print(current_reliability, incongruent_observations, total_valid_observations)
    return current_reliability - (current_reliability * (incongruent_observations / total_valid_observations))


def find_first_congruent(list_of_observations):
    for i in range(len(list_of_observations)):
        if list_of_observations[i].shape.congruent == True:
            return i


def sql_query(query):
    # Åpne tilkobling til database
    con = connect_to_db()
    cur = con.cursor()

    # Kjør SQL og lagre resultatet
    cur.execute(query)
    result = cur.fetchall()

    # Lukk tilkoblingen til databasen
    cur.close()
    con.close()

    return result



def get_observations_from_db(id: int):
    # SQL for å hente data fra databasen som GeoJSON
    observations = sql_query('''
        SELECT id, type, dato, st_asgeojson(geom) as geom, name, geoid
        FROM observasjon
        WHERE geoid = %d 
        ORDER BY dato; 
        '''%id)
    
    obs = []

    for row in observations:
        obs.append(Observation(row[0], row[1], row[2], row[3], row[5]))

    return obs


def get_latest_observation(geoid: int) -> Observation:
    latest_observation = sql_query('''
        SELECT id, type, dato, st_asgeojson(geom) as geom, geoid
        FROM observasjon
        WHERE geoid = %d
        ORDER BY dato desc
        LIMIT 1;
    '''%geoid)[0]

    return Observation(latest_observation[0], latest_observation[1], latest_observation[2], latest_observation[3], latest_observation[4])



if __name__ == "__main__":    
    # test = Observation(1, "flyfoto", datetime.datetime.now(), {"x":69, "y":420})

    # print(vars(test))
    # print(vars(test.shape))

    #print( config )
    print("Reliability: ", round(find_reliability( get_latest_observation(69) ), 4))
    #print( get_latest_observation(69).ID )