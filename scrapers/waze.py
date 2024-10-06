import requests
import json

def get_waze_data(toLocation, fromLocation):
    baseUrl = "https://www.waze.com/live-map/api/user-drive?geo_env=na"
    reqData  = {
        "from":{"y":fromLocation["lat"],"x":fromLocation["lng"]},"to":{"y":toLocation["lat"],"x":toLocation["lng"]},
         "nPaths":3,
         "useCase":"LIVEMAP_PLANNING",
         "interval":15,
         "arriveAt":True
         
    }
    
    response = requests.post(baseUrl, json=reqData)
    parseData = parse_waze_data(response.json())
    return parseData


def parse_waze_data(wazeData):
    pathObj = {
        "timeSeconds": wazeData["alternatives"][0]["response"]["totalSeconds"],
        "distanceMeters": wazeData["alternatives"][0]["response"]["totalLength"],
        "coords": []
    }
    for coord in wazeData["alternatives"][0]["coords"]:
        pathObj["coords"].append({"lat":coord["y"],"lng":coord["x"]})

    return pathObj


