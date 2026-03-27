from flask import Flask, jsonify
#this import is to connect routes to main.py
from flask import Blueprint
import psycopg2

app = Flask (__name__)

#variable to import into main.py
weather_bp = Blueprint('weather', __name__)

def get_db_connection(): 
    conn = psycopg2.connect(
        dbname = "weatherTracker_DB_CSIS-1230", 
        user = "postgres", 
        password = "Ti@ncas07", 
        host = "localhost", 
        port = "5432"
    )
    return conn

@weather_bp.route('/')
def home():
    return "Welcome to Weather Tracker"

@weather_bp.route('/weather', methods = ['POST'])
def create_weather(): 
    return "Create a new weather report"

#FLASK IMPLEMENTATION (post) 
@weather_bp.route('/weather', methods=['GET'])
def get_all_weather(): 
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM observations")
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

    return jsonify(weather_list)

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
    
    return jsonify({ 
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

@weather_bp.route('/weather/<int:id>', methods = ['PUT'])
def update_weather(id): 
    return f"Update weather report {id}"

@weather_bp.route('/weather/<int:id>', methods = ['DELETE'] )
def delete_weather(id): 
    return f"Delete weather report {id}"