try:
    from datetime import datetime, UTC
    import weather as w
    import json
    import statistics as st

    datetime.now()

except (SyntaxError, ImportError, NameError) as synt_err:
     print(f"  [warn] Environment is not ready or Import has failed: {synt_err}")

except Exception as e:
     print(f"  [warn] Environment is not ready or Import has failed: {e}")


def to_float(value, default=None):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

def fetched_at():

    return datetime.now(UTC).isoformat()


def fetch_all_cities(cities):

    cities_list = []

    for city in cities:
        try:
            raw_name = city.get("name")
            city_name = str(raw_name).strip().capitalize() if raw_name else ""
            
            lat = to_float(city.get("lat"))
            if lat < -90.0 or lat > 90.0:
                print(f"   [warn] fetch_all_cities(): Latitude out of range: {lat}")
                continue

            lon = to_float(city.get("lon"))
            if lon < -180.0 or lon > 180.0:
                print(f"   [warn] fetch_all_cities(): Logitude out of range: {lon}")
                continue
            
            if city_name and  lat is not None and lon is not None:
                current_weather = w.get_weather(lat, lon) or ""
                
                if isinstance(current_weather, dict) and current_weather:
                    
                    weather_info = {
                        "city" : city_name,
                        "fetched_at" : fetched_at(),
                        "weather" : current_weather
                    }
                    cities_list.append(weather_info)
        except (TypeError, AttributeError) as error:
            print(f"   [warn] fetch_all_cities(): {error}")
            continue
                
    if len(cities_list) > 0:
        return cities_list
    else:
        return []


if __name__ == "__main__":
    cities = [ 
        {"name": "Sydney", "lat": -33.87, "lon": 151.21}, 
        {"name": "Melbourne", "lat": -37.81, "lon": 144.96}, 
        {"name": " melbourne", "lat": -37.81, "lon": 144.96},
        {"name": "Brisbane", "lat": -27.47, "lon": 153.02},
        
    ] 

    print(fetch_all_cities(cities))

