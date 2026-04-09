'''
Mark Chechott & Skylar Thompson
CSCE 4050/5050
Project: Secure RESTful Communication
SERVER
'''

from Crypto.Hash import HMAC, SHA256
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from flask import Flask, jsonify, request
import json
import base64

app = Flask(__name__) # creates instance of Flask application

XY = 39 # last two digits of Skylar's Student ID

#loading the secret and public keys into storage
with open("secret.key", "rb") as f:
    private_key = RSA.import_key(f.read())

with open("public.key", "rb") as f:
    public_key = RSA.import_key(f.read())

#initializing the session key
session_key = None

# added endpoint to send the certificate to the client
@app.route("/certificate", methods=["GET"])
def get_certificate():
    try:
        with open("pk.cert", "rb") as f:
            cert_data = f.read()
        cert_b64 = base64.b64encode(cert_data).decode("utf-8")
        return jsonify({"certificate": cert_b64}), 200
    except FileNotFoundError:
        return jsonify({"error": "Certificate file not found on server"}), 404


#sending the public key
@app.route("/public-key", methods=["GET"])
def get_public_key():
    public_key_text = public_key.export_key().decode("utf-8")
    return jsonify({"public_key": public_key_text})


#Receiving the encrypted session key
@app.route("/session-key", methods=["POST"])
def receive_session_key():
    global session_key
    
    data = request.get_json()

    if not data or "encrypted_key" not in data:
        return jsonify({"error": "No encrypted key"}), 400
    
    try:
        encrypted_key = base64.b64decode(data["encrypted_key"])
        
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(encrypted_key)

        return jsonify({"message": "Session key received"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to decrypt session key: {str(e)}"}), 400


@app.route("/weather", methods=["GET"]) # defines the route
def weather(): # the content to be returned 
    global session_key

    if session_key is None:
        return jsonify({"error": "Session key has not been established yet"}), 403
    
    data = {
        "location": "Denton, TX",
        "temperature_c": 10,
        "temperature_f": 50,
        "condition": "Partly Cloudy",
        "humidity_percent": XY
    }

    # force keys to be in alphabetical order
    plaintext = json.dumps(data, sort_keys=True).encode("utf-8") #Converting json to bytes
    
    # use AECGCM because it provides encryption confidentiality and authentication
    cipher = AES.new(session_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    payload = {
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    }

    return jsonify(payload) 

if __name__ == "__main__":
    port = 5000 + XY
    print(f"Server running at http://127.0.0.1:{port}/weather")
    print(f"CA Certificate: http://127.0.0.1:{port}/certificate")
    print(f"Public key endpoint: http://127.0.0.1:{port}/public-key")
    print(f"Session key endpoint: http://127.0.0.1:{port}/session-key")
    print(f"Weather endpoint: http://127.0.0.1:{port}/weather")
    
    app.run(host="127.0.0.1", port=port) # starts the server
