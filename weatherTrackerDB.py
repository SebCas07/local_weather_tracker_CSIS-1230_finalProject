import psycopg2 

def save_to_db (report): 
    conn = psycopg2.connect(
        dbName = "weatherTracker_DB_CSIS-1230",
        user = "=",
        password = "Ti@ncas07",
        host = "localhost", 
        port = "5432"
    )

    cur = conn.cursor()

    cur.execute(""" INSERT INTO observations (city, country, latitude, longitude, temperature, elvation, windspeed, observation_time) 
                VALUES(%s, %s, %s, %s, %s, %s, %s , %s)""", 
                (
                 report.city, 
                 report.country,
                 report.latitude, 
                 report.longitude, 
                 report.temperature, 
                 report.elevation, 
                 report.windspeed, 
                 report.observation_time 
                 ))

    conn.commit()
    cur.close()
    conn.close()


