'''
Mark Chechott & Skylar Thompson
CSCE 4050/5050
Project: Secure RESTful Communication
CLIENT
'''

import requests
import json
import base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import unpad
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15

url = "http://127.0.0.1:5039"

# endpoints
cert_url = f"{url}/certificate"
public_key_url = f"{url}/public-key"
session_key_url = f"{url}/session-key"
weather_url = f"{url}/weather"

# certification verification
try:
    # get certificate from server
    cert_response = requests.get(cert_url)
    if cert_response.status_code != 200:
        print("Failed to fetch certificate.")
        exit()
        
    cert_raw = base64.b64decode(cert_response.json()["certificate"])

    # split message + signature using '||SIGNATURE||' separator
    message, signature = cert_raw.split(b"||SIGNATURE||")

    # load the public key
    with open("public_ca.key", "rb") as f:
        ca_public_key = RSA.import_key(f.read())

    # verify signature using SHA256
    h = SHA256.new(message)
    pkcs1_15.new(ca_public_key).verify(h, signature)
    
    print("Certificate verified. Server identity confirmed.")
    print(f"Identity Message: {message.decode('utf-8')}")

except (ValueError, TypeError):
    print("Certificate invalid! The server cannot be trusted.")
    exit()
except Exception as e:
    print(f"An error occurred during verification: {e}")
    exit()


#Getting the server public key
response = requests.get(public_key_url)

if response.status_code != 200:
    print(f"Failed to get public key: {response.status_code}")
    exit()

server_public_key_text = response.json()["public_key"]
server_public_key = RSA.import_key(server_public_key_text)

print("Received server public key.")


#Generate random session key
session_key = get_random_bytes(32) # AES-256
print("Generated random AES session key.")

#Ecnrypt session with RSA
cipher_rsa = PKCS1_OAEP.new(server_public_key)
encrypted_session_key = cipher_rsa.encrypt(session_key)

encrypted_key_b64 = base64.b64encode(encrypted_session_key).decode("utf-8")


#Send encrypted session key to the server
response = requests.post(session_key_url, json={
    "encrypted_key": encrypted_key_b64
})

if response.status_code != 200:
    print(f"Failed to send session key: {response.status_code}")
    print(response.text)
    exit()

print("Encrypted session is key sent to the server.")

#request encrypted weather data

response = requests.get(weather_url)

if response.status_code == 200:
    # record responses to response.bin
    with open("response.bin", "wb") as f:
        f.write(response.content)

    payload = response.json()
    nonce = base64.b64decode(payload["nonce"])
    ciphertext = base64.b64decode(payload["ciphertext"])
    tag = base64.b64decode(payload["tag"])

    # decrypt and authenticate
    cipher = AES.new(session_key, AES.MODE_GCM, nonce=nonce)
   
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        data = json.loads(plaintext.decode("utf-8"))
        print("Success. Decrypted data:", data)

    except ValueError:
        print("Data tampered or MAC invalid.")

else:
    print(f"Error: {response.status_code}")
