from pya3 import *
from pymongo import MongoClient
import json
from datetime import datetime
from time import sleep

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['token_data']

alice = Aliceblue(user_id='AB093838', api_key='cy5uYssgegMaUOoyWy0VGLBA6FsmbxYd0jNkajvBVJuEV9McAM3o0o2yG6Z4fEFYUGtTggJYGu5lgK89HumH3nBLbxsLjgplbodFHDLYeXX0jGQ5CUuGtDvYKSEzWSMk')
print(alice.get_session_id()) # Get Session ID
LTP = 0
socket_opened = False
subscribe_flag = False
subscribe_list = []
unsubscribe_list = []

def save_to_mongodb(token, data):
    collection_name = f'token_{token}'  # Create collection name based on the token
    collection = db[collection_name]
    collection.insert_one(data)
    print(f"Data saved for token {token}")

def socket_open():
    print("Connected")
    global socket_opened
    socket_opened = True
    if subscribe_flag:
        alice.subscribe(subscribe_list)

def socket_close():
    global socket_opened, LTP
    socket_opened = False
    LTP = 0
    print("Closed")

def socket_error(message):
    global LTP
    LTP = 0
    print("Error :", message)

def feed_data(message):
    global LTP, subscribe_flag
    feed_message = json.loads(message)
    if feed_message["t"] == "ck":
        print("Connection Acknowledgement status :%s (Websocket Connected)" % feed_message["s"])
        subscribe_flag = True
        print("subscribe_flag :", subscribe_flag)
        print("-------------------------------------------------------------------------------")
        pass
    elif feed_message["t"] == "tk":
        print("Token Acknowledgement status :%s " % feed_message)
        print("-------------------------------------------------------------------------------")
        pass
    else:
        print("Feed :", feed_message)
        if 'lp' in feed_message:
            token = feed_message.get('tk')  # Assuming 'token' is the correct identifier for the token
            if token:
                save_to_mongodb(token, feed_message)
            else:
                print("Token not found in feed message.")

alice.start_websocket(socket_open_callback=socket_open, socket_close_callback=socket_close,
                      socket_error_callback=socket_error, subscription_callback=feed_data, run_in_background=True,
                      market_depth=False)

while not socket_opened:
    pass

# Example tokens
tokens = [44152, 44159, 44160, 44161, 44162, 44163, 44164, 44171, 44172, 44183]

subscribe_list = [alice.get_instrument_by_token('NFO', token) for token in tokens]
alice.subscribe(subscribe_list)
print(datetime.now())
sleep(10)
print(datetime.now())

while True:
    sleep(1) 