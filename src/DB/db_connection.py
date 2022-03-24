import psycopg2

import sys
sys.path.append('/home/eirik/git/azure/NorkartBachelor')

from src.config import config


# configure database parameters in database.ini file. Template: /src/DB/databaseTemplate.ini

def connect_to_db(database_config='database.ini'):
    conn = None

    try:
        params = config(database_config)

        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn
