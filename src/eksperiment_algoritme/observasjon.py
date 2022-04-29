from common import config, sql_query
import datetime
import eksperiment_biou as biou
from shapely.geometry import Polygon
from itertools import chain
import json
import numpy


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
        self.BIOU = biou.measure_biou(self.polygon, new_observation.shape.polygon)
        self.congruent = True if self.BIOU > float(config['iouthreshold']) else False
        return self.congruent


# Funksjon som finner observasjoner som er enige med den nyeste observasjonen.
def find_reliability_oldest_agreeing(new_observation: Observation):
    # Hente observasjoner fra databasen.
    list_of_observations = get_observations_from_db(new_observation.geoid)

    for obs in list_of_observations:
        obs.shape.update_comparison(new_observation)

    # Liste over observasjoner fra den første som er enig. (Lista er sortert kronologisk)
    valid_observations = list_of_observations[find_first_congruent(list_of_observations):]

    return calculate_reliability(new_observation, valid_observations)


# Funksjon som finner observasjoner hvor det brukes standardavvik på gjennomsnittlig BIoU
def find_reliability_st_dev_mean(new_observation: Observation):
    # Hente observasjoner fra databasen. (Eldste først)
    list_of_observations = get_observations_from_db(new_observation.geoid)

    # Variabel som holder på gjennomsnitts-BIoU resultatene
    average_scores = []
    
    # For hver observasjon sammenligne med tidligere observasjoner
    for index in range(len(list_of_observations)):
        obs = list_of_observations[index]
        bious = []
        for o in list_of_observations[:index]:
            obs.shape.update_comparison(o)
            bious.append(obs.shape.BIOU)

        if bious:
            average_scores.append(sum(bious)/len(bious))
    del(index)

    # Regn ut standardavviket på BIoU-resultatene, gang det med verdien i config
    stdev = numpy.std(average_scores) * int(config['splittingdeviation'])
    
    # Definer terskelen for observasjoner som skal være inkludert i utregningen videre
    line = max(average_scores) - stdev

    for index in range(len(average_scores)):
        score = average_scores[index]
        if(score < line):
            # Avslutt løkken, da vi kun er interessert i den første observasjonen under terskelen
            break

    # Regn ut BIoU på nytt mot observasjonen vi leter etter påliteligheten for
    for valid_obs in list_of_observations[index+1:]:
        valid_obs.shape.update_comparison(new_observation)

    return calculate_reliability(new_observation, list_of_observations[index+1:])


# Funksjon som finner observasjoner hvor det brukes standardavvik mot en satt grense i config.ini
def find_reliability_st_dev(new_observation: Observation):
    # Hente observasjoner fra databasen. (Eldste først)
    list_of_observations = get_observations_from_db(new_observation.geoid)

    # Variabel som holder på gjennomsnitts-BIoU resultatene
    row_stdevs = []
    
    # For hver observasjon sammenligne med tidligere observasjoner
    for index in range(len(list_of_observations)):
        obs = list_of_observations[index]
        bious = []
        for o in list_of_observations[:index]:
            obs.shape.update_comparison(o)
            bious.append(obs.shape.BIOU)

        if bious:
            row_stdevs.append(numpy.std(bious))
    del(index)

    # Her setter vi "streken" fra config.ini-fila.
    threshold = float(config['stdevstatic'])

    for index in range(len(row_stdevs)):
        score = row_stdevs[index]
        if(score > threshold):
            # Avslutt løkken, da vi kun er interessert i den første observasjonen over terskelen
            break

    # Regn ut BIoU på nytt mot observasjonen vi leter etter påliteligheten for
    for valid_obs in list_of_observations[index+1:]:
        valid_obs.shape.update_comparison(new_observation)
        
    return calculate_reliability(new_observation, list_of_observations[index+1:])


def calculate_reliability(ref_observation: Observation, valid_observations: list[Observation]):
    # Diverse variabler med utgansgpunkt settes
    next_multiplier = 0.5
    incongruent_observations = 0
    total_valid_observations = 0

    # Setter utgangspunktet for pålitelighet basert på dataset. forhåndsdefinert i config.
    current_reliability = float(config['basereliability' + ref_observation.dataset ])
    
    for obs in valid_observations:
        if obs.ID != ref_observation.ID: # Hopp over matten hvis ID-en er den samme som den som sammenlignes mot
            # Hvis observasjonen er enig i endringen, øk påliteligheten i samsvar med "next multiplier", og halverer multiplier til neste gang.
            if obs.shape.congruent:
                current_reliability = current_reliability + (current_reliability * next_multiplier)
                next_multiplier = next_multiplier / 2
            else:
                incongruent_observations += 1
            total_valid_observations += 1

    if total_valid_observations < 1:
        print("Not enough data to create reliability score")
        return 0
    else:
        return current_reliability - (current_reliability * (incongruent_observations / total_valid_observations))


def find_first_congruent(list_of_observations):
    for i in range(len(list_of_observations)):
        if list_of_observations[i].shape.congruent == True:
            return i


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
    observation_id = 69
    print("Measure reliability for observation-id: ", observation_id)
    print("Reliability: ", round( find_reliability_oldest_agreeing( get_latest_observation(observation_id) ), 4), "(from oldest agreeing observation)")
    print("Reliability: ", round( find_reliability_st_dev_mean(     get_latest_observation(observation_id) ), 4), "(from standard-deviation on mean)")
    print("Reliability: ", round( find_reliability_st_dev(          get_latest_observation(observation_id) ), 4), "(from standard-deviation by threshold)")
