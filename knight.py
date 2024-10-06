from flask import Flask, jsonify, render_template, request
from scrapers import waze, gmaps, amaps
from sqldb import db

app = Flask(__name__)

@app.route('/')
def serveHtml():
    return render_template("index.html")

@app.route('/route-data',methods = ['POST'])
# /data endpoint
def data():
    # get data from waze
    request_data = request.get_json()
    #data = waze.get_waze_data(request_data["to"], request_data["from"])
    appleData = amaps.get_apple_data(request_data["to"], request_data["from"])
    googleData = gmaps.get_google_data(request_data["to"], request_data["from"])
    wazeData = waze.get_waze_data(request_data["to"], request_data["from"])

    data = {
        "apple": appleData,
        "google": googleData,
        "waze": wazeData
    }
    db(data)
    return data

if __name__ == '__main__':
    app.run(debug=True)


    
    
#est travel time
#series of cords



