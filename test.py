from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Weather Tracker"

@app.route('/weather', methods=['GET'])
def get_all_weather(): 
    return "Get all weather reports"

if __name__ == '__main__':
    app.run(debug=True)