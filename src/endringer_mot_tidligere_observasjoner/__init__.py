import json
from common import config

from src.DB.db_connection import connect_to_db
import observasjon as o

# Denne filen inneholder diverse tester som er kjørt. For de ferdige testene se i observasjon.py

if __name__ == "__main__":
    # open connection
    con = connect_to_db()

    # open cursor
    cur = con.cursor()

    # SQL for å hente data fra databasen som GeoJSON
    getObjects = '''
        SELECT id, type, dato, st_asgeojson(geom) as geom, name
        FROM observasjon
        ORDER BY dato; 
        '''

    # Kjør SQL og lagre resultatet i observations
    cur.execute(getObjects)
    observations = cur.fetchall()

    # Lagre den nyeste observasjonen i sisteObservasjon
    sisteObservasjon = o.Observation(
        observations[-1][0],
        observations[-1][1],
        observations[-1][2],
        json.loads(observations[-1][3]))

    for row in observations:
        ob = o.Observation(row[0], row[1], row[2], json.loads(row[3]))
        enighet = ob.shape.update_comparison(sisteObservasjon)

        #iou = sa.measure_iou_of_observations(sisteObservasjon, o)
        #enighet = " ENIG" if iou > IOUthreshold else "UENIG"
        print("Observasjon med navn \"%s\" av type '%s' er %s (BIoU: %s)"%(row[4], row[1], enighet, ob.shape.BIOU))


    # close cursor
    cur.close()

    # close connection
    con.close()
