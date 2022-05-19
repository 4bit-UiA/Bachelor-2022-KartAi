from src.DB.db_connection import connect_to_db
from shapely_eksperimentering import load_observations_from_file
import geojson

if __name__ == "__main__":
    # open connection
    con = connect_to_db('../DB/database.ini')

    # open cursor
    cur = con.cursor()

    # insert mock-data into database
    ###############################################################################################
    # observations = load_observations_from_file("../../resources/observasjoner_2020.json") \
    #                + load_observations_from_file("../../resources/observasjoner_2021.json") \
    #                + load_observations_from_file("../../resources/observasjoner_2022.json")
    #
    # for o in observations:
    #     gj = o.geojson
    #     dataset = gj['properties']['dataset']
    #     date = gj['properties']['date']
    #     cur.execute("""INSERT INTO observations (dataset, date, geom)
    #                    VALUES (%s, %s, (ST_GeomFromGeoJSON(%s)));""",
    #                 (dataset, date, geojson.dumps(gj['geometry'])))
    #
    # con.commit()
    ###############################################################################################

    area_of_observations = """ 
        SELECT id, date, dataset, ST_Area(geography(geom), false) as area
        FROM observations
        ORDER BY date; 
        """

    hausdorff_distance = """
        SELECT ST_HausdorffDistance(%s, %s);
    """

    hausdorff_distance_with_ids = """
        SELECT ST_HausdorffDistance(
            (SELECT geom from observations where id = %s), 
            (SELECT geom from observations where id = %s)
        );
        """

    frechet_distance_with_ids = """
        SELECT ST_FrechetDistance(
            (SELECT geom from observations where id = %s), 
            (SELECT geom from observations where id = %s)
        );
    """

    frechet_distance = """
            SELECT ST_FrechetDistance(%s, %s);
        """

    center_polygons = """
        WITH pt AS (SELECT geom from observations where id = 85),
            poly as (SELECT * from observations)
        SELECT poly.dataset, poly.date, ST_Translate(
                poly.geom,
                st_x(pt.geom) - st_x(st_centroid(poly.geom)),
                st_y(pt.geom) - st_y(st_centroid(poly.geom))
            )
        from pt, poly
        ORDER BY poly.date;
    """

    cur.execute(area_of_observations)
    areas = cur.fetchall()
    for a in areas:
        print(a)
        # for b in areas:
        #     cur.execute(frechet_distance, (a[0], b[0]))
        #     print(cur.fetchone())

    # cur.execute(center_polygons)
    # areas = cur.fetchall()
    # for a in areas:
    #     print(a[0], a[1])
    #     for b in areas:
    #         cur.execute(hausdorff_distance, (a[2], b[2]))
    #         print(cur.fetchone(), b[0], b[1])
    #     print("")

    # close cursor
    cur.close()

    # close connection
    con.close()
