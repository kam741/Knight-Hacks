from flask import Flask, jsonify, request, make_response
from testScrape import scrape_power_outage_data  # Import the scrape function
from FloridaCountiesDictionary import florida_counties
import json

# Open and load the JSON file

app = Flask(__name__)


# add user database hookup here
users = {
    "admin": "password123",
}

valid_tokens = {}

# Function to verify token
def token_required(f):
    def wrap(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token not in valid_tokens.values():
            return jsonify({'message': 'Authentication required'}), 401
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__  # Fix for Flask's function naming
    return wrap

# Root endpoint just returning 200 status
@app.route('/')
def home():
    return make_response('', 200)

# /data endpoint to return some sample data needs actual data
@app.route('/data', methods=['GET'])
def data():
    with open('stateData.json', 'r') as file:
        data = json.load(file)

    return jsonify(data)

# Login endpoint to authenticate and return token
@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    username = auth.get('username')
    password = auth.get('password')

    # check in DB here
    if username in users and users[username] == password:
        # For simplicity, use the username as the token
        token = f'token-{username}'
        valid_tokens[username] = token
        return jsonify({'token': token})

    return make_response('Invalid credentials', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

# /post-data endpoint that requires authentication hook up to db
@app.route('/post-data', methods=['POST'])
@token_required
def post_data():
    data = request.json
    return jsonify({'message': 'Data posted successfully', 'data': data})

@app.route('/get-county-code', methods=['POST'])
def get_county_code():
    data = request.get_json()
    county_name = data.get('countyName', '').lower()

    if county_name in florida_counties:
        county_code = florida_counties[county_name]
        scrape_power_outage_data(county_code, county_name)  # Call the scraping function (data will be saved to JSON)
        return jsonify({'countyCode': county_code})  # Just return the county code
    else:
        return jsonify({'error': 'County not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
