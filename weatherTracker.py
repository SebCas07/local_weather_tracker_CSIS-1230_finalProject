#imports listed below
#requirement of text (look up to generate after installing libraries *create it after you finish*)
import requests
# testing flask implementation from week 7  
from flask import Flask

app = Flask(__name__)

#geocoding endpoint that converts city name to lattitude/longitude 
def get_coordinates(city, country): 

    #{city}, {country}, {count} in URL one var so that when ran the url changes as the city and country change with the users input 
    URL_One = "https://geocoding-api.open-meteo.com/v1/search?name={city}&country={country}&count={count}"

    #side note: params was named "data" however this wouldnt work because I had a later line that attributed data var with response.json 
                #for future reference make sure params var name isnt accidentally assigned to something else down the road. 
    params = { 
        "name": city, 
        "country": country, 
        "count": 1 
    }  

    response = requests.get(URL_One, params=params)
    data = response.json()

    if "results" not in data: 
        raise Exception("City not found")
    
    result = data["results"][0]

    return{ 
        "city": result["name"], 
        "country": result["country"], 
        "latitude": result["latitude"], 
        "longitude": result["longitude"]
    }


#method that passes the retrieved latitude and longitude as parameters to retrieve the following weather
# information: city, country, latitude, longitude, temperature, elevation, windspeed, and observation time.

def get_weather(latitude, longitude): 
    URL_Two = "https://api.open-meteo.com/v1/forecast?current_weather=true"

    params = { 
        "latitude": latitude,
        "longitude": longitude, 
        "current_weather": "True"
    }

    response = requests.get(URL_Two, params=params) 
    data = response.json()

    #test for test case 2 
    # return data
    current = data["current_weather"]
    
    #switch between current and data in some lines because of the json structure
    #look at test case 2 
    return{ 
        "temperature": current["temperature"],
        "elevation": data["elevation"], 
        "windspeed": current["windspeed"], 
        "observation_time": current["time"] 
    }



class WeatherReport: 
    def __init__(self, city, country, latitude, longitude, temperature, elevation, windspeed, observation_time): 
        self.city = city
        self.country = country 
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = temperature
        self.elevation = elevation 
        self.windspeed = windspeed
        self.observation_time = observation_time

    def __str__(self): 
        return (
            f"Weather Report\n"
            f"City: {self.city}, {self.country}\n"
            f"Latitude: {self.latitude}\n"
            f"longitude: {self.longitude}\n"
            f"Temperature: {self.temperature} Celsius\n"
            f"Elevation: {self.elevation}m\n"
            f"Wind Speed: {self.windspeed}km/h\n"
            f"Observation Time: {self.observation_time}"
        )

   
#setting variables 
city = "Chicago"
country = "US"

#Qcalling methods
coords = get_coordinates(city, country)
weather = get_weather(coords["latitude"], coords["longitude"]) 

#print out structure

report = WeatherReport( 
    coords["city"], 
    coords["country"],
    coords["latitude"],
    coords["longitude"], 
    weather["temperature"], 
    weather["elevation"], 
    weather["windspeed"], 
    weather["observation_time"]
)

@app.route('/')
def results(): 
    return str(report)
 
print(report)
#test case ONE
# print(get_coordinates("San Diego", "US"))
#test case TWO (looking at json structurre to ensure return call works)

# weather_data = get_weather(32.72, -117.16)

# print(json.dumps(weather_data, indent=4))

#FLASK implementation 
if __name__ == '__main__': 
    app.run(debug=True)