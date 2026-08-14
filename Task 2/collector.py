# ----------------------
# Assessment 3 - Task 2
# Utility functions for validating city coordinates, fetching weather data,
# and maintaining a JSON log of weather records.
# Student: Raphael Barbosa Maciel
# Subject: AI Programming Fundamentals (COMP90100_2026_OT4_UMO_1)
# GitHub repo: https://github.com/raphaelmaciel-unimelb/Assessment-3
# ---------------------

try:
    from datetime import datetime, UTC
    import weather as w
    import json
    import statistics as st
    from dotenv import load_dotenv
    
    load_dotenv()

except (SyntaxError, ImportError, NameError) as synt_err:
     print(f"  [warn] Environment is not ready or Import has failed: {synt_err}")

except Exception as e:
     print(f"  [warn] Environment is not ready or Import has failed: {e}")


def to_float(value, default=None):
    """Convert a value to a float or return a fallback value.

    This helper safely attempts float conversion for values such as strings
    or numeric inputs that may be missing or malformed.

    Args:
       value: The value to convert to a float.
       default: The fallback value returned if conversion fails.

    Returns:
       The float representation of the value, or the provided default if the
       conversion is not possible.
    """
    try:
       return float(value)
    except (TypeError, ValueError):
       return default

def fetched_at():
    """Return the current UTC timestamp in ISO 8601 format.

    This function generates a timestamp suitable for logging weather fetches
    and comparing the recency of data collection events.

    Returns:
       A UTC timestamp string in ISO 8601 format.
    """
    return datetime.now(UTC).isoformat()


def fetch_all_cities(cities):
    """Validate city coordinates, fetch weather data, and return valid records.

    Each item in the input list is checked for a valid city name and coordinate
    range before a weather request is made. Only records with valid weather
    responses are returned.

    Args:
       cities: A list of dictionaries containing city metadata, including name,
           latitude, and longitude.

    Returns:
       A list of dictionaries containing the city name, fetch timestamp, and
       weather response data for valid cities only.
    """

    cities_list = []

    for city in cities:
        try:
            # Normalise the city name before checking the weather request details.
            raw_name = city.get("name")
            city_name = str(raw_name).strip().capitalize() if raw_name else ""

            # Check whether the latitude is within the accepted global range.
            lat = to_float(city.get("lat"))
            if lat < -90.0 or lat > 90.0:
                print(f"   [warn] fetch_all_cities(): Latitude out of range: {lat}")
                continue

            # Check whether the longitude is within the accepted global range.
            lon = to_float(city.get("lon"))
            if lon < -180.0 or lon > 180.0:
                print(f"   [warn] fetch_all_cities(): Longitude out of range: {lon}")
                continue

            # Only request and store weather info when the city and coordinates are valid.
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



def update_log(log_path, new_results):
    """Load the current weather log, append valid records, and save the file.

    Existing entries are read from the JSON log if present. New records are
    checked for required fields before being appended and written back to disk.

    Args:
        log_path: The file path to the JSON weather log.
        new_results: A list of weather record dictionaries to add to the log.

    Returns:
        True if the log was successfully written; otherwise False.
    """

    list_results=[]

    try:
        # Load any earlier records already stored in the weather log.
        with open(log_path, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                    if content:
                        json_content = json.loads(content)
                        if isinstance(json_content, list):
                            for item in json_content:
                                if isinstance(item, dict) and item.get('city'):
                                    list_results.append(item)

    except (AttributeError, FileNotFoundError, json.decoder.JSONDecodeError) as file_not_found:
        print(f"   [warn] update_log(): {file_not_found} ... trying to create the file if the folder is available")

    # Keep only records that contain a valid city, fetch timestamp, and weather payload.
    for result in new_results:
        raw_city = result.get('city')
        result_city = str(raw_city).strip().capitalize() if raw_city else ""
        result_fetched_at = result.get('fetched_at')
        result_weather = result.get('weather')

        if result_city not in ("", None) and result_fetched_at not in ("", None) and result_weather:
            new_record = dict(result)
            new_record["city"] = result_city
            list_results.append(new_record)

    if len(list_results) > 0:
        try:
            # Persist the combined list as JSON for later summary and reuse.
            with open(log_path, "w", encoding="utf-8") as outfile:
                json.dump(list_results, outfile, indent=2, ensure_ascii=False) #converting list[dict] to json and adding to the output file
        except Exception as e:
            print(f"   [error] update_log(): Error with the file {log_path}: {e}")
            return False

        return True
    else:
        return False

def summarise_log(log_path):
    """Summarise the weather log by counting records and calculating summary metrics.

    This function reads the saved weather log, filters out incomplete entries,
    and returns the total number of records, unique cities tracked, the latest
    fetch timestamp, and the average temperature across valid readings.

    Args:
        log_path: The file path to the JSON weather log to summarise.

    Returns:
        A dictionary containing total_records, cities_tracked, latest_fetch,
        and avg_temperature.
    """

    list_results=[]

    try:
        # Load the JSON weather log so the summary can be rebuilt from stored records.
        with open(log_path, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                    if content:
                        json_content = json.loads(content)
                        if isinstance(json_content, list):
                            list_results = json_content

    except (AttributeError, FileNotFoundError, json.decoder.JSONDecodeError) as file_not_found:
        print(f"   [Error] summarise_log() File error: {file_not_found}")
        return {}


    # Collect the fields needed for a summary across all valid weather entries.
    city_set= set()
    fetched_at_list=[]
    temperature_list=[]
    
    for result in list_results:
        try:
            if not isinstance(result, dict):
                continue
            
            city = str(result.get("city", "")).strip().capitalize()
            fetched_at_val = result.get("fetched_at")
            
            weather_data = result.get("weather", {})
            temp_val = weather_data.get("temperature") if isinstance(weather_data, dict) else None
            temperature = to_float(temp_val)

            if city and fetched_at_val and temperature is not None:
                city_set.add(city)
                fetched_at_list.append(fetched_at_val)
                temperature_list.append(temperature)

        except Exception as e:
            print(f"   [warn] summarise_log record skipped: {e}")
            continue
    
    # If city, time stamp, and temperature lists are valid, create the summary
    if city_set and fetched_at_list and temperature_list:
        return {
            "total_records" : len(list_results),
            "cities_tracked" : sorted(list(city_set)),
            "latest_fetch" : max(fetched_at_list),
            "avg_temperature" : round(st.mean(temperature_list),2)
        }
    
    # Otherwise, returns an empty summary report
    return {
        "total_records": 0,
        "cities_tracked": [],
        "latest_fetch": None,
        "avg_temperature": None
    }     



if __name__ == "__main__":
    cities = [ 
        {"name": "Sydney", "lat": -33.87, "lon": 151.21}, 
        {"name": "Melbourne", "lat": -37.81, "lon": 144.96}, 
        {"name": " melbourne", "lat": -37.81, "lon": 144.96},
        {"name": "Brisbane", "lat": -27.47, "lon": 153.02},
        
    ] 

    update_log("weather_log.json", fetch_all_cities(cities)) 

    new = [ 
        {"city": "Sydney", 
        "fetched_at": "2026-05-24T05:05:52+00:00", 
        "weather": {"temperature": 18.4, "windspeed": 12.3, 
                    "winddirection": 180, "weathercode": 3, 
                    "time": "2026-05-24T14:00"}},
        {"city": " Sydney", 
        "fetched_at": "2026-05-24T05:05:52+00:00", 
        "weather": {"temperature": 18.4, "windspeed": 12.3, 
                    "winddirection": 180, "weathercode": 3, 
                    "time": "2026-05-24T14:00"}} 
    ] 


    update_log("weather_log.json", new)
    summary = summarise_log("weather_log.json")
    print(summary)
