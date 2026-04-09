'''
Mark Chechott & Skylar Thompson
CSCE 4050/5050
Project: Secure RESTful Communication
CLIENT
'''

import time
import requests
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import HMAC, SHA256

Hard_Coded_Key = b"9f4c2b7d8a1e3f6c4d7a9b21e5c0f8d3"  
Max_Drift = 5 #number of seconds a message can be off by


url = "http://127.0.0.1:5039/weather"

response = requests.get(url)


if response.status_code == 200:
    # record responses to response.bin
    with open("response.bin", "wb") as f:
        f.write(response.content)

    payload = response.json()
    nonce = base64.b64decode(payload["nonce"])
    ciphertext = base64.b64decode(payload["ciphertext"])
    tag = base64.b64decode(payload["tag"])

    # decrypt and authenticate
    cipher = AES.new(Hard_Coded_Key, AES.MODE_GCM, nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        data = json.loads(plaintext.decode("utf-8"))

        message_time = data.get("timestamp", 0)
        current_time = int(time.time())

        if abs(current_time - message_time) > Max_Drift:
            print("Replay or stale message detected!")
        else:
            print("Success. Decrypted data:", data)

    except ValueError:
        print("Data tampered or MAC invalid.")

else:
    print(f"Error: {response.status_code}")
