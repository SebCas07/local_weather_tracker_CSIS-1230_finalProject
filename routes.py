from flask import jsonify, render_template, request, redirect, url_for
#this import is to connect routes to main.py
from flask import Blueprint
import psycopg2
import os 
from dotenv import load_dotenv
import requests

load_dotenv()

#variable to import into main.py
weather_bp = Blueprint('weather', __name__, template_folder='templates')

def get_db_connection(): 
    conn = psycopg2.connect(
        dbname = os.getenv('DB_NAME'), 
        user = os.getenv('DB_USER'), 
        password = os.getenv('DB_PASSWORD'), 
        host = os.getenv('DB_HOST'), 
        port = os.getenv('DB_PORT')
    )
    return conn

@weather_bp.route('/')
def home():
    return render_template('home_weather.html')

@weather_bp.route('/weather/add', methods = ['GET'])
def add_weather_form(): 
    return render_template('add_weather.html')

@weather_bp.route('/weather', methods = ['POST'])
def create_weather(): 
    city = request.form.get('city')
    country = request.form.get('country')

    #call the geocoding API
    geo_response=requests.get('https://geocoding-api.open-meteo.com/v1/search', params = {
        "name": city, 
        "country": country, 
        "count": 1 
    })
    geo_data=geo_response.json()

    if "results" not in geo_data: 
        return "City not found", 404
    
    result = geo_data["results"][0]
    latitude = result["latitude"]
    longitude = result["longitude"]
    city_name = result["name"]
    country_name = result["country"]

    #call the weather API
    weather_response = requests.get('https://api.open-meteo.com/v1/forecast', params={ 
        "latitude": latitude, 
        "longitude": longitude, 
        "current_weather" : True
    })

    weather_data = weather_response.json()
    current = weather_data["current_weather"]

    # insert into DB
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute("""
                INSERT INTO observations (city, country, latitude, longitude, temperature, elevation, windspeed, observation_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (city) DO NOTHING """, (
                    city_name, 
                    country_name, 
                    latitude, 
                    longitude, 
                    current['temperature'], 
                    weather_data['elevation'], 
                    current['windspeed'], 
                    current['time']
                ))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('weather.get_all_weather'))

@weather_bp.route('/weather/<int:id>/edit', methods=['GET'])
def edit_weather(id): 
    conn = get_db_connection()
    cur = conn.cursor()

    # fetches the fresh weather data from the API using existing coords
    cur.execute("SELECT * FROM observations WHERE id = %s", (id,))
    row = cur.fetchone()

    if row is None: 
        return "Record not found", 404
    
    weather = { 
        "id": row[0], 
        "city": row[1], 
        "country": row[2],
        "latitude": row[3], 
        "longitude": row[4], 
        "temperature": row[5], 
        "elevation": row[6], 
        "windspeed": row[7], 
        "observation_time": row[8]
    }

    return render_template('edit_weather.html', weather = weather)

@weather_bp.route('/weather/<int:id>/delete', methods=['POST'])
def delete_weather(id): 
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM observations WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('weather.get_all_weather'))

#FLASK IMPLEMENTATION (post) 
@weather_bp.route('/weather', methods=['GET'])
def get_all_weather(): 
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM observations ORDER BY ID")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    weather_list = []
    for row in rows: 
        weather_list.append({
            "id": row[0], 
            "city": row[1], 
            "country": row[2], 
            "latitude": row[3], 
            "longitude": row[4], 
            "temperature": row[5], 
            "elevation": row[6], 
            "windspeed": row[7], 
            "observation_time": row[8]
        })

    return render_template('weather.html', weather_list = weather_list)

@weather_bp.route('/weather/<int:id>', methods = ['GET'])
def get_weather_by_id(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM observations WHERE id = %s", (id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None: 
        return jsonify({"error": "Record not found"}), 404
    
    weather = { 
        "id": row[0], 
        "city": row[1], 
        "country": row[2], 
        "latitude": row[3], 
        "longitude": row[4], 
        "temperature": row[5], 
        "elevation": row[6], 
        "windspeed": row[7], 
        "observation_time": row[8]
    }

    return render_template ('weather_detail.html', weather=weather)

@weather_bp.route('/weather/<int:id>/edit', methods = ['POST'])
def update_weather(id): 
    city = request.form.get('city')
    country = request.form.get('country')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    temperature = request.form.get('temperature')
    elevation = request.form.get('elevation')
    windspeed = request.form.get('windspeed')
    observation_time = request.form.get('observation_time')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
                UPDATE observations
                SET city = %s, country=%s, latitude = %s, longitude = %s, 
                temperature = %s, elevation = %s, windspeed = %s, observation_time = %s
                WHERE id = %s
                """, (
                    city, country, latitude, longitude, temperature, elevation, windspeed, observation_time, id 
                ))
    
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('weather.get_all_weather'))

# @weather_bp.route('/weather/<int:id>', methods = ['DELETE'] )
# def delete_weather(id): 
#     return f"Delete weather report {id}"