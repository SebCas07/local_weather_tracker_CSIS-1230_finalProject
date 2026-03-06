
from flask import Flask

app = Flask(__name__)

#FLASK IMPLEMENTATION (post) 
@app.route('/weather', methods = ['POST'])
def create_weather(): 
    return "Create a new weather report"

#FLASK IMPLEMENTATION (post) 
@app.route('/weather', methods=['GET'])
def get_all_weather(): 
    return "Get all weather reports"

@app.route('/weather/<int:id>', methods = ['GET'])
def get_weather(id):
    return f"Get weather report {id}"

@app.route('/weather/<int:id>', methods = ['PUT'])
def update_weather(id): 
    return "Update weather report {id}"

@app.route('/weather/<int:id>', methods = ['DELETE'] )
def delete_weather(id): 
    return f"Delete weather report {id}"