import sys
import os
sys.path.append(os.getcwd() + "/../../")
from src.config import config as conf

config = conf("config.ini", "algoritme")


def sql_query(query):
    # Hent databasetilkoblingen til prosjektet
    from src.DB.db_connection import connect_to_db

    # Åpne tilkobling til database
    con = connect_to_db('../DB/database.ini')
    cur = con.cursor()

    # Kjør SQL og lagre resultatet
    cur.execute(query)
    result = cur.fetchall()

    # Lukk tilkoblingen til databasen
    cur.close()
    con.close()

    return result
