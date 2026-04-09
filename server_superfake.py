'''
Mark Chechott & Skylar Thompson
CSCE 4050/5050
Project: Secure RESTful Communication
SUPER FAKE SERVER
'''

from flask import Flask, send_file

app = Flask(__name__)
XY = 39

@app.route("/weather", methods=["GET"])
def weather():
    # only send the exact binary file captured earlier
    return send_file("response.bin", mimetype='application/json')

if __name__ == "__main__":
    # Port XY = 5039
    app.run(host="127.0.0.1", port=5039)
