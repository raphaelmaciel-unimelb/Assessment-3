import requests, json

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather(latitude, longitude):
    """Fetch the current weather for one location from the Open-Meteo API.

    Sends each coordinate to the API, requesting temperatures in
    Celsius.

    Args:
        latitude:  Latitude of the location.
        longitude: Longitude of the location.

    Returns:
        On a successful response (HTTP status == 200), the full
        current-weather dict (temperature, windspeed, winddirection,
        time, ...) exactly as the API returns it.

        On any other status, prints the status code and returns None.
    """    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "temperature_unit": "celsius",    
        "timezone": "auto"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["current_weather"]

    else:
        print(f"API error: {response.status_code}")
        return None

def save_to_file(city, data, filename):
    """Write a weather payload to `filename` as JSON.

    Produces a record with two keys: a "city" label and a "data" field
    holding `data` directly as the weather dict.

    Args:
        data:     The current-weather dict returned by get_weather().
        filename: Path of the JSON file to write.
    """    
    record = {
        "city": city,
        "data": [data] 
    }
    with open(filename, "w") as f:
        json.dump(record, f, indent=2)

result = get_weather(-33.87, 151.21)  # Sydney
save_to_file('Sydney', result, "weather_output.json")
print("Done.")
