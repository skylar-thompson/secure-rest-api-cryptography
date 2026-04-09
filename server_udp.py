'''
Mark Chechott & Skylar Thompson
CSCE 4050/5050
Project: Secure RESTful Communication
Reference: https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application
SERVER
'''

from Crypto.Hash import HMAC, SHA256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from flask import Flask, jsonify
import json
import base64
import time #Used for a timestamp on the json file

Hard_Coded_Key = b"9f4c2b7d8a1e3f6c4d7a9b21e5c0f8d3"  

app = Flask(__name__) # creates instance of Flask application

XY = 39 # last two digits of Skylar's Student ID

@app.route("/weather", methods=["GET"]) # defines the route
def weather(): # the content to be returned 
    data = {
        "location": "Denton, TX",
        "temperature_c": 10,
        "temperature_f": 50,
        "condition": "Partly Cloudy",
        "humidity_percent": XY,
        "timestamp": int(time.time())
    }

    # force keys to be in alphabetical order
    plaintext = json.dumps(data, sort_keys=True).encode("utf-8") #Converting json to bytes
    

    # use AECGCM because it provides encryption confidentiality and authentication
    cipher = AES.new(Hard_Coded_Key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)



    payload = {
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    }

    return jsonify(payload) 

if __name__ == "__main__":
    port = 5000 + XY # "port runs on 50XY"
    print(f"Server running at http://127.0.0.1:{port}/weather")
    app.run(host="127.0.0.1", port=port) # starts the server
