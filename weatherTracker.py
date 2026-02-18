#imports listed below
#requirement of text (look up to generate after installing libraries *create it after you finish*)
import requests

#geocoding endpoint that converts city name to lattitude/longitude 
def get_coordinates(city, country): 
    URL_One = "https://geocoding-api.open-meteo.com/v1/search?name={city}&country={country}&count={count}"

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


URL_Two = "https://api.open-meteo.com/v1/forecast?current_weather=true"


print(get_coordinates("San Diego", "US"))