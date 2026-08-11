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



def update_log(log_path, new_results):

        list_results=[]

        try:
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
            # return False              

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
                with open(log_path, "w", encoding="utf-8") as outfile:
                    json.dump(list_results, outfile, indent=2, ensure_ascii=False) #converting list[dict] to json and adding to the output file
            except Exception as e:
                print(f"   [error] update_log(): Error with the file {log_path}: {e}")
                return False          

            return True     
        else:
            return False

def summarise_log(log_path):

    list_results=[]

    try:
        with open(log_path, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                    if content:
                        json_content = json.loads(content)
                        if isinstance(json_content, list):
                            list_results = json_content
                            
    except (AttributeError, FileNotFoundError, json.decoder.JSONDecodeError) as file_not_found:
        print(f"   [Error] summarise_log() File error: {file_not_found}")
        return {}              

    

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
                    
    if city_set and fetched_at_list and temperature_list:
        return {
            "total_records" : len(list_results),
            "cities_tracked" : sorted(list(city_set)),
            "latest_fetch" : max(fetched_at_list),
            "avg_temperature" : round(st.mean(temperature_list),2)
        }
    
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
