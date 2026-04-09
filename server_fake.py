'''
Mark Chechott & Skylar Thompson
CSCE 4050/5050
Project: Secure RESTful Communication
FAKE SERVER
'''

from flask import Flask, jsonify
import json

app = Flask(__name__) # creates instance of Flask application

XY = 39 # last two digits of Skylar's Student ID

@app.route("/weather", methods=["GET"]) # defines the route
def weather(): # the content to be returned 
    fakeData = {
        "location": "Denton, TX",
        "temperature_c": 10,
        "temperature_f": 50,
        "condition": "Partly Cloudy",
        "humidity_percent": XY + 1
    }

    # attacker reuses tag intercepted from step 3 in the tag.txt file
    with open("tag.txt", "r") as f:
        interceptedTag = f.read().strip()
    
    payload = {
    "data": fakeData,
    "mac": interceptedTag
    }

    return jsonify(payload) 

if __name__ == "__main__":
    port = 5000 + XY + 1  # port runs on 5000 + XY + 1
    print(f"Malicious server running at http://127.0.0.1:{port}/weather")
    app.run(host="127.0.0.1", port=port) # starts the server
