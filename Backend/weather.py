import requests

def get_metar(station):
    url = f"https://avwx.rest/api/metar/{station}"
    headers = {"Authorization": "NqeMiDKymD4VjT9epVakwJrQgBkDLutjqymAw2vFkoM"}
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["raw"]
    

import requests

def get_wx_info(station, request):
    url = f"https://avwx.rest/api/metar/{station}"
    headers = {"Authorization": "NqeMiDKymD4VjT9epVakwJrQgBkDLutjqymAw2vFkoM"}
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        if request == "time":
            return data["time"]["dt"] if "time" in data else "Missing time data"

        elif request == "temperature":
            return data["temperature"]["value"] if "temperature" in data else "Missing temperature data"

        elif request == "altimeter":
            return data["altimeter"]["value"] if "altimeter" in data else "Missing altimeter data"

        elif request == "visibility":
            return data["visibility"]["value"] if "visibility" in data else "Missing visibility data"

        elif request == "remarks":
            return ", ".join(data["remarks"]) if "remarks" in data and isinstance(data["remarks"], list) else "No remarks"

        elif request == "clouds":
            return ", ".join(item["repr"] for item in data["clouds"]) if "clouds" in data and isinstance(data["clouds"], list) else "No cloud data"

        elif request == "wx_codes":
            return ", ".join(item["value"] for item in data["wx_codes"]) if "wx_codes" in data and isinstance(data["wx_codes"], list) else "No weather codes"

        elif request == "wind":
            return f"Wind {data['wind_direction']['value']}° at {data['wind_speed']['value']} knots" if "wind_direction" in data and "wind_speed" in data else "Missing wind data"

        elif request == "dew_point":
            return data["dewpoint"]["value"] if "dewpoint" in data else "Missing dew point data"

        elif request == "pressure":
            return data["sea_level_pressure"]["value"] if "sea_level_pressure" in data else "Missing pressure data"

        elif request == "humidity":
            return data["relative_humidity"] if "relative_humidity" in data else "Missing humidity data"

        elif request == "icao":
            return data["station"] if "station" in data else "Missing ICAO data"

        elif request == "raw_metar":
            return data["raw"] if "raw" in data else "Missing raw METAR data"

        elif request == "flight_category":
            return data["flight_rules"] if "flight_rules" in data else "Missing flight category data"

        elif request == "station":
            return data["station"] if "station" in data else "Missing station data"

        elif request == "pressure_tendency":
            return data["remarks_info"]["pressure_tendency"]["tendency"] if "remarks_info" in data and "pressure_tendency" in data["remarks_info"] else "Missing pressure tendency data"

        elif request == "maximum_temperature_6":
            return data["remarks_info"]["maximum_temperature_6"]["value"] if "remarks_info" in data and "maximum_temperature_6" in data["remarks_info"] else "Missing max temperature data"

        elif request == "minimum_temperature_6":
            return data["remarks_info"]["minimum_temperature_6"]["value"] if "remarks_info" in data and "minimum_temperature_6" in data["remarks_info"] else "Missing min temperature data"

        elif request == "density_altitude":
            return data["density_altitude"] if "density_altitude" in data else "Missing density altitude data"

        elif request == "pressure_altitude":
            return data["pressure_altitude"] if "pressure_altitude" in data else "Missing pressure altitude data"

        elif request == "sunshine_minutes":
            return data["remarks_info"]["sunshine_minutes"] if "remarks_info" in data and "sunshine_minutes" in data["remarks_info"] else "No sunshine data"

        elif request == "snow_depth":
            return data["remarks_info"]["snow_depth"] if "remarks_info" in data and "snow_depth" in data["remarks_info"] else "No snow depth data"

        else:
            return f"Invalid request: {request}"

    return "Error fetching data"

