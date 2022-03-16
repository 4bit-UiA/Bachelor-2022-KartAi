import json
from src.DB.db_connection import connect_to_db
import src.eksperiment_johannes.similarity_analysis as sa

# Threshold(s) for å si om tidligere målinger er like
IOUthreshold = 0.95

if __name__ == "__main__":
    # open connection
    con = connect_to_db('../DB/database.ini')

    # open cursor
    cur = con.cursor()

    # SQL for å hente data fra databasen som GeoJSON
    getObjects = """ 
        SELECT id, dato, name, ST_AsGeoJSON(geom), type as geojson
        FROM observasjon
        ORDER BY dato desc; 
        """

    cur.execute(getObjects)
    observations = cur.fetchall()


    sisteObservasjon = sa.Observation(observations[0][1],
                                      None,
                                      None,
                                      None,
                                      None,
                                      json.loads(observations[0][3]))

    for row in observations:
        o = sa.Observation(row[1],
                           None,
                           None,
                           None,
                           None,
                           json.loads(row[3]))
        iou = sa.measure_iou_of_observations(sisteObservasjon, o)
        enighet = " ENIG" if iou > IOUthreshold else "UENIG"
        print("Observasjon med navn \"%s\" av type '%s' er %s (IOU: %s)"%(row[2], row[4], enighet, iou))


    # close cursor
    cur.close()

    # close connection
    con.close()
