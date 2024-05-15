from flask import Flask, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId, json_util
import json
import pandas as pd
from datetime import datetime

app = Flask(__name__)
<<<<<<< HEAD
CORS(app)
=======
>>>>>>> 4fcc10db2e34928b362b1a8877306394207c8eb5

def parse_json(data):
    return json.loads(json_util.dumps(data))

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string in a specific format
        return json.JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder  # Set the custom JSON encoder for the Flask app

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['token_data_22']

tokens = [41558, 41561, 41568, 41569, 41572, 41573, 41574, 41576, 41577, 41610, 41615, 41616, 41617, 41620, 41621, 41638]
df = pd.read_csv('NFO.csv')

# Filter the DataFrame to only include rows with the specified token numbers
filtered_df = df[df['Token'].isin(tokens)]

# Extract the strike price, option type, and token for each token number
strike_prices = filtered_df[['Strike Price', 'Option Type', 'Token']]
<<<<<<< HEAD
strike_prices.to_csv('updated_NFO.csv', index=False)
=======
>>>>>>> 4fcc10db2e34928b362b1a8877306394207c8eb5

print(strike_prices)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    response_data = {}  # Initialize an empty dictionary to store response data
    for token in tokens:
        collection_name = f'token_{token}'  # Create collection name based on the token
        collection = db[collection_name]
        # Assuming 'timestamp' is the field name in MongoDB for the last updated time
        data = collection.find_one(sort=[('_id', -1)])  # Sort by _id in descending order to get the latest document
        if data:
            parsed_data = parse_json(data)
            response_data[token] = {'status': 'success', 'data': parsed_data, 'timestamp': data.get('timestamp', 'N/A')}
        else:
            response_data[token] = {'status': 'error', 'message': 'Data not found'}

    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True, port=8009)
