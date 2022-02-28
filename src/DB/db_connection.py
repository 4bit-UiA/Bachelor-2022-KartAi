import psycopg2
from src.config import config


# configure database parameters in database.ini file. Template: /src/DB/databaseTemplate.ini

def connect_to_db():
    conn = None

    try:
        params = config()

        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn
