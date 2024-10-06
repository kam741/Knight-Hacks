import requests
import polyline

API_KEY = ""

def get_google_data(start, end):
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    
    startLoc = f"{start['lat']},{start['lng']}"
    endLoc = f"{end['lat']},{end['lng']}"
    
    params = {
        "origin": startLoc,
        "destination": endLoc,
        "key": API_KEY
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return parse_response(response.json())
    else:
        raise Exception(f"Error in API request: {response.status_code}")

def parse_response(data):

    route = data['routes'][0]
    leg = route['legs'][0]
    time_seconds = leg['duration']['value']
    distance_meters = leg['distance']['value']
    coordinates = []
    
    for step in leg['steps']:
        polyline_points = step['polyline']['points']
        decoded_points = polyline.decode(polyline_points) 
        coordinates.extend(decoded_points) 

    return {
        "timeSeconds": time_seconds,
        "distanceMeters": distance_meters,
        "coords": [{"lat": lat, "lng": lng} for lat, lng in coordinates] 
    }

