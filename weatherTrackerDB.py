import psycopg2 
import os 
from dotenv import load_dotenv

# loads the .env file
load_dotenv()

def save_to_db (report): 
    conn = psycopg2.connect(
        dbname = os.getenv('DB_NAME'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        host = os.getenv("DB_HOST"), 
        port = os.getenv('DB_PORT')
    )

    cur = conn.cursor()

    cur.execute(""" INSERT INTO observations (city, country, latitude, longitude, temperature, elevation, windspeed, observation_time) 
                VALUES(%s, %s, %s, %s, %s, %s, %s , %s) 
                ON CONFLICT (city) DO NOTHING""",
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


