from flask import Flask
#this import is to connect routes to main.py
from flask import blueprints

app = Flask (__name__)

#variable to import into main.py
weather_bp = blueprints('weather', __name__)

@app.route('/')
def home():
    return "Welcome to Weather Tracker"

@app.route('/weather', methods = ['POST'])
def create_weather(): 
    return "Create a new weather report"

#FLASK IMPLEMENTATION (post) 
@app.route('/weather', methods=['GET'])
def get_all_weather(): 
    return "Get all weather reports"

@app.route('/weather/<int:id>', methods = ['GET'])
def get_weather_by_id(id):
    return f"Get weather report {id}"

@app.route('/weather/<int:id>', methods = ['PUT'])
def update_weather(id): 
    return f"Update weather report {id}"

@app.route('/weather/<int:id>', methods = ['DELETE'] )
def delete_weather(id): 
    return f"Delete weather report {id}"