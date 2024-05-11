from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json
import pandas as pd

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder  # Set the custom JSON encoder for the Flask app

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['token_data']

tokens = [44152, 44159, 44160, 44161, 44162, 44163, 44164, 44171, 44172, 44183]
df = pd.read_csv('NFO.csv')

# Filter the DataFrame to only include rows with the specified token numbers
filtered_df = df[df['Token'].isin(tokens)]

# Extract the strike price for each token number
strike_prices = filtered_df['Strike Price']

print(strike_prices)

@app.route('/get_data', methods=['GET'])
def get_data():
    response_data = {}  # Initialize an empty dictionary to store response data
    for token in tokens:
        collection_name = f'token_{token}'  # Create collection name based on the token
        collection = db[collection_name]
        data = collection.find_one()  # Assuming you want to fetch one document
        if data:
            response_data[token] = {'status': 'success', 'data': data}
        else:
            response_data[token] = {'status': 'error', 'message': 'Data not found'}

    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True, port=8009)
