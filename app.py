from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId, json_util
import json
import pandas as pd

app = Flask(__name__)

def parse_json(data):
    return json.loads(json_util.dumps(data))

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder  # Set the custom JSON encoder for the Flask app

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['token_data']

tokens = [44152, 44159, 44160, 44161, 44162, 44163, 44164, 44171, 44172, 44183]
df = pd.read_csv('NFO.csv')

# Filter the DataFrame to only include rows with the specified token numbers
filtered_df = df[df['Token'].isin(tokens)]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    response_data = {}  # Initialize an empty dictionary to store response data
    for token in tokens:
        collection_name = f'token_{token}'  # Create collection name based on the token
        collection = db[collection_name]
        data = collection.find_one()  # Assuming you want to fetch one document
        if data:
            # Use json_util to parse MongoDB data (if needed)
            parsed_data = parse_json(data)
            response_data[token] = {'status': 'success', 'data': parsed_data}
        else:
            response_data[token] = {'status': 'error', 'message': 'Data not found'}

    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(debug=True, port=8009)
