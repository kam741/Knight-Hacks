import requests
import json

def get_apple_data(toLocation, fromLocation):
    baseUrl = "https://beta.maps.apple.com/data/direction"
    reqData  =  {
    "destinationLocation": {
        "waypointPlaceInfo": {
            "roadAccessPoints": [
                {
                    "location": {
                        "lat": toLocation["lat"],
                        "lng": toLocation["lng"]
                    },
                    "isApproximate": True,
                    "walkingDirection": "ENTRY_EXIT",
                    "drivingDirection": "ENTRY_EXIT"
                }
            ],
            "mapRegion": {
                "southLat": 0,
                "westLng": 0,
                "northLat": 0,
                "eastLng": 0,
                "mapRegionSourceType": "REV_POLYGON_FIT"
            }
        },
        "waypointNameProperties": {
            "hasSpokenName": False,
            "hasSpokenAddress": False,
            "hasDisplayName": True,
            "hasDisplayAddress": True
        },
        "location": {
            "latitude": toLocation["lat"],
            "longitude": toLocation["lng"]
        }
    },
    "startLocation": {
        "waypointPlaceInfo": {
            "roadAccessPoints": [
                {
                    "location": {
                        "lat": fromLocation["lat"],
                        "lng": fromLocation["lng"]
                    },
                    "isApproximate": True,
                    "walkingDirection": "ENTRY_EXIT",
                    "drivingDirection": "ENTRY_EXIT"
                }
            ],
            "mapRegion": {
                "southLat": 0,
                "westLng": 0,
                "northLat": 0,
                "eastLng": 0,
                "mapRegionSourceType": "REV_POINT_PADDED"
            }
        },
        "location": {
            "latitude": fromLocation["lat"],
            "longitude": fromLocation["lng"]
        }
    },
    "dirflg": "d",
    "analyticMetadata": {
        "appIdentifier": "com.apple.MapsWeb",
        "appMajorVersion": "1",
        "appMinorVersion": "1.89",
        "isInternalInstall": False,
        "isFromAPI": False,
        "requestTime": {
            "timeRoundedToHour": 749851563,
            "timezoneOffsetFromGmtInHours": 4
        },
        "serviceTag": {
            "tag": "0"
        },
        "hardwareModel": "Windows",
        "osVersion": "Windows NT 10.0",
        "productName": "Windows",
        "sessionId": {
            "high": 0,
            "low": 0
        },
        "relativeTimestamp": 0,
        "sequenceNumber": 0
    },
    "dcc": "US"
    }
    
    response = requests.post(baseUrl, json=reqData)
    respObj = parse_lat_lng(response.json())
    return respObj


def parse_lat_lng(json_data):
    # List to store lat/lng values along with distance and traversal time
    routes_info = {
        "timeSeconds": 0,
        "distanceMeters": 0,
        "coords": []
    }
    
    # Check if "waypointRoute" exists and if it has any routes
    if "waypointRoute" in json_data and len(json_data["waypointRoute"]) > 0:
        # Access the first route
        first_route = json_data["waypointRoute"][0]
        
        # Iterate through routeLegs in the first route
        for routeleg in first_route["routeLeg"]:
            # Extract distance and expected time from route leg
            routes_info["distanceMeters"] = routeleg.get("distance", 0)  # Adjust based on actual key for distance if needed
            routes_info["timeSeconds"] = routeleg.get("expectedTime", 0)  # Adjust based on actual key for time if needed
            
            # Iterate through decodedPathLeg in each route leg
            for leg in routeleg.get("decodedPathLeg", []):
                # Extract lat/lng from the location key
                location = leg.get("location", {})
                lat = location.get("lat")
                lng = location.get("lng")
                
                # Ensure both lat and lng are present
                if lat is not None and lng is not None:
                    # Append the extracted information
                    routes_info["coords"].append({
                        "lat": lat,
                        "lng": lng,
                    })
                    
    
    return routes_info
