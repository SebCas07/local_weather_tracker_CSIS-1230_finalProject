from flask import Flask
#this import is to connect routes to main.py
from flask import Blueprint

app = Flask (__name__)

#variable to import into main.py
weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/')
def home():
    return "Welcome to Weather Tracker"

@weather_bp.route('/weather', methods = ['POST'])
def create_weather(): 
    return "Create a new weather report"

#FLASK IMPLEMENTATION (post) 
@weather_bp.route('/weather', methods=['GET'])
def get_all_weather(): 
    return "Get all weather reports"

@weather_bp.route('/weather/<int:id>', methods = ['GET'])
def get_weather_by_id(id):
    return f"Get weather report {id}"

@weather_bp.route('/weather/<int:id>', methods = ['PUT'])
def update_weather(id): 
    return f"Update weather report {id}"

@weather_bp.route('/weather/<int:id>', methods = ['DELETE'] )
def delete_weather(id): 
    return f"Delete weather report {id}"